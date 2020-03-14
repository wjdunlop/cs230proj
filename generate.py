import numpy as np
import music21
import train

def generate(X, gen_length, weights_name, encoding_size, num_notes):
    model = train.get_model(X, encoding_size)
    model.load_weights(weights_name)

    initial_seq_idx = np.random.randint(X.shape[0])
    sequence = X[initial_seq_idx]

    num_instruments = sequence.shape[1]
    sequence = sequence.reshape(1, sequence.shape[0], num_instruments)
    output = []
    for i in range(gen_length):
        print(i, '/', gen_length, end = '\r', flush = True)
        prediction = model.predict(sequence)
        new_elem = np.argmax(prediction)
        sequence[:, 0:sequence.shape[1] - 1, :] = sequence[:, 1:, :]
        sequence[:, sequence.shape[1] - 1, :] = new_elem
        output.append(new_elem)
    return output

def convert_int_to_sequence(note_seq, decoder):

    print(note_seq)
    
    tokenSeq = []
    for note in note_seq:
        # print(decoder)
        n = decoder[note]
        tokenSeq.append(n)
    # print(tokenSeq)
    return tokenSeq

def sequence_to_notes(score, sample_freq):
    
    # code adapted from Clara.
    
    speed = 1./sample_freq
    notes = []
    time_offset = 0
    
    for i in range(len(score)):
        if score[i] in ["", " ", "<eos>", "<unk>"]:
            continue
        elif score[i][:3]=="end":
            if score[i][-3:]=="eoc":
                time_offset+=1
            continue
        elif score[i][:4]=="wait":
            time_offset+=int(score[i][4:])
            continue
        else:
            # Look ahead to see if an end<noteid> was generated
            # soon after.  
            duration=1
            has_end=False
            note_string_len = len(score[i])
            for j in range(1,200):
                if i+j==len(score):
                    break
                if score[i+j][:4]=="wait":
                    duration+=int(score[i+j][4:])
                if score[i+j][:3+note_string_len]=="end"+score[i] or score[i+j][:note_string_len]==score[i]:
                    has_end=True
                    break


            if not has_end:
                duration=12

            add_wait = 0

            try: 
                # print(score[i][1:])
                new_note=music21.note.Note(int(score[i][1:]))

                new_note.duration = music21.duration.Duration(duration*speed)
                new_note.offset=time_offset*speed
                notes.append(new_note)                
            except:
                print("Unknown note: " + score[i])
            # time_offset+=add_wait           
    #change below here for multi-instrument
    trumpet=music21.instrument.fromString("Trumpet")
    notes.insert(0, trumpet)    
    trumpet_stream=music21.stream.Stream(notes)
    # main_stream = music21.stream.Stream([violin_stream, piano_stream])
    return trumpet_stream
