import os
import music21
import keras
from music21 import converter, instrument, note, chord
import numpy as np
import music21
songpath_solo = "./songdata/solo/Trumpet in Bb"

# credit to Clara's music generator for this encoding method
def create_chordwise_rep(midi, maxNote, numInstruments, sampleRate):
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


def append_modulations(input, output, input_seq, output_seq, wait_token_begin, augment_dataset):
    input.append(input_seq)
    output.append(output_seq)
    if augment_dataset:
        original_input = np.asarray(input_seq)
        for modulation in range(-5, 7):
            augmented_input = np.where(original_input < wait_token_begin, original_input + modulation, original_input)
            augmented_output = output_seq + modulation if output_seq < wait_token_begin else output_seq
            # if sequence is all rests, avoid weighting this too heavily by inserting 12 times
            if np.array_equal(augmented_input, original_input) and augmented_output == output_seq:
                continue
            input.append(augmented_input.tolist())
            output.append(augmented_output)

def build_dataset(sequences, wait_token_begin, sequence_length, augment_dataset):
    input = []
    output = []
    for sequence in sequences:
        for i in range(0, len(sequence) - sequence_length):
            append_modulations(input, output, sequence[i:i+sequence_length], sequence[i+sequence_length],
                               wait_token_begin, augment_dataset)

    num_examples = len(input)
    X = np.asarray(input, dtype=int).reshape((num_examples, sequence_length, 1))
    y = keras.utils.to_categorical(output, num_classes=wait_token_begin + 24)
    return X, y

def collect_solo_songs(convert_dict, max_note, num_instruments, sample_rate, sequence_length, augment_dataset):
    wait_token_begin = convert_dict["wait1"]
    note_seqs = []
    for _, _, files in os.walk(songpath_solo):
        for file in files:
            print("Parsing " + file)
            midi = converter.parse(songpath_solo + "/" + file)

            chordwise_seq = create_chordwise_rep(midi, max_note, num_instruments, sample_rate)
            note_seq = chords_to_notes(chordwise_seq, sample_rate)
            note_seqs.append(convert_sequence_to_int(note_seq, convert_dict))
    return build_dataset(note_seqs, wait_token_begin, sequence_length, augment_dataset)