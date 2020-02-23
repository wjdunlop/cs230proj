import os
import music21
from music21 import converter, instrument, note, chord
import numpy as np

songpath_solo = "./songdata/solo/Trumpet in Bb"

# credit to Clara's music generator for this encoding method
def create_chordwise_rep(midi, maxNote, numInstruments, sampleRate):
    # parse_notes = None
    # parts = instrument.partitionByInstrument(midi)
    # if parts:
    #     parse_notes = parts.parts[0].recurse()
    # else:
    #     parse_notes = midi.flat.notesAndRests
    #
    # for element in parse_notes:
    #     # print(element)
    #     # print(element.duration.quarterLength)
    #     # print(element.offset)
    #     if isinstance(element, note.Note):
    #         print(element.pitch.midi)
    maxTime = int(np.floor(midi.duration.quarterLength * sampleRate) + 1)
    score = np.zeros((maxTime, numInstruments, maxNote))

    noteFilter = music21.stream.filters.ClassFilter('Note')
    for note in midi.recurse().addFilter(noteFilter):
        pitch = note.pitch.midi
        offset = int(np.floor(note.offset * sampleRate))
        duration = int(np.floor(note.duration.quarterLength * sampleRate))
        score[offset, 0, pitch] = 1
        score[offset+1:offset+duration, 0, pitch] = 2

    instr = {}
    instr[0] = "t"
    chordwise = []
    for timestep in score:
        for i in list(reversed(range(len(timestep)))):
            chordwise.append(instr[i] + ''.join([str(int(note)) for note in timestep[i]]))

    return chordwise

def chords_to_notes(chords, sample_rate):
    notes = []
    for chordIdx in range(len(chords)):
        chord = chords[chordIdx]
        futureChord = ""
        for futureChordIdx in range(chordIdx + 1, len(chords)):
            if chords[futureChordIdx][0] == chord[0]:
                futureChord = chords[futureChordIdx]
                break
        instrument = chord[0]
        chord = chord[1:]
        futureChord = futureChord[1:]
        for pitch in range(len(chord)):
            # if pitch not being played we don't care
            if chord[pitch] == "0":
                continue

            # if pitch active, we do
            note = instrument + str(pitch)
            if chord[pitch] == "1":
                notes.append(note)

            # pitch continued to play, if it ends next, add an end instruction
            if futureChord == "" or futureChord[pitch] == "0":
                notes.append("end" + note)

        notes.append("wait")

    # collect the wait terms
    note_seq = ""
    idx = 0
    while idx < len(notes):
        wait_count = 1
        if notes[idx] == "wait":
            while wait_count <= sample_rate * 2 and idx + wait_count < len(notes) and notes[idx + wait_count] == "wait":
                wait_count += 1
            # avoid stepping over index
            if wait_count > sample_rate * 2:
                wait_count -= 1
            notes[idx] = "wait" + str(wait_count)
        note_seq += notes[idx] + " "
        idx += wait_count

    return note_seq

def convert_sequence_to_int(sequence, convert_dict):
    note_tokens = sequence.split(' ')
    encodings = []
    for token in note_tokens:
        if len(token) > 0:
            encodings.append(convert_dict[token])
    return encodings

def build_dataset(sequences, sequence_length = 40):
    input = []
    output = []
    for sequence in sequences:
        for i in range(0, len(sequence) - sequence_length):
            input.append(sequence[i:i+sequence_length])
            output.append(sequence[i+sequence_length])
    print(input)
    print(output)

def collect_solo_songs(convert_dict, max_note, num_instruments, sample_rate):
    note_seqs = []
    for _, _, files in os.walk(songpath_solo):
        for file in files:
            print("Parsing " + file)
            midi = converter.parse(songpath_solo + "/" + file)

            chordwise_seq = create_chordwise_rep(midi, max_note, num_instruments, sample_rate)
            note_seq = chords_to_notes(chordwise_seq, sample_rate)
            note_seqs.append(convert_sequence_to_int(note_seq, convert_dict))
    return build_dataset(note_seqs)