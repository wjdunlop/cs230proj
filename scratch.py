import pickle

X = pickle.load(open("x.pickle", "rb"))
y = pickle.load(open('y.pickle', 'rb'))

print(X[:10])
print(y[:10])



# import datacollector
# import utils
# import music21
# from music21 import converter, instrument, note, chord
# songpath_solo = "./songdata/solo/Trumpet in Bb"
# midi = converter.parse(songpath_solo + '/563_trumpet_voluntary_Trumpet in Bb.mid')
# max_note = 127
# num_instruments = 1
# sample_rate = 12
# note_seqs = []
# convert_dict, decoder = utils.build_convert_dict(max_note, ['t'], sample_rate)
# chordwise_seq = datacollector.create_chordwise_rep(midi, max_note, num_instruments, sample_rate)
# note_seq = datacollector.chords_to_notes(chordwise_seq, sample_rate)
# note_seqs.append(datacollector.convert_sequence_to_int(note_seq, convert_dict))

# # print(note_seqs)

# def convert_int_to_sequence(note_seq, decoder):

# 	tokenSeq = []
# 	for note in note_seq:
# 		note1 = decoder[note]
# 		tokenSeq.append(note1)
# 	print(tokenSeq)
# 	return tokenSeq

# def sequence_to_notes(score, sample_freq):
	
# 	# code adapted from Clara.

	
#     speed = 1./sample_freq
#     notes = []
#     time_offset = 0
    
#     for i in range(len(score)):
#         if score[i] in ["", " ", "<eos>", "<unk>"]:
#             continue
#         elif score[i][:3]=="end":
#             if score[i][-3:]=="eoc":
#                 time_offset+=1
#             continue
#         elif score[i][:4]=="wait":
#             time_offset+=int(score[i][4:])
#             continue
#         else:
#             # Look ahead to see if an end<noteid> was generated
#             # soon after.  
#             duration=1
#             has_end=False
#             note_string_len = len(score[i])
#             for j in range(1,200):
#                 if i+j==len(score):
#                     break
#                 if score[i+j][:4]=="wait":
#                     duration+=int(score[i+j][4:])
#                 if score[i+j][:3+note_string_len]=="end"+score[i] or score[i+j][:note_string_len]==score[i]:
#                     has_end=True
#                     break


#             if not has_end:
#                 duration=12

#             add_wait = 0

#             try: 
#                 print(score[i][1:])
#                 new_note=music21.note.Note(int(score[i][1:]))

#                 new_note.duration = music21.duration.Duration(duration*speed)
#                 new_note.offset=time_offset*speed
#                 notes.append(new_note)                
#             except:
#                 print("Unknown note: " + score[i])
#             # time_offset+=add_wait


                
#     #change below here for multi-instrument
#     trumpet=music21.instrument.fromString("Trumpet")
#     notes.insert(0, trumpet)	
#     trumpet_stream=music21.stream.Stream(notes)
#     # main_stream = music21.stream.Stream([violin_stream, piano_stream])
#     return trumpet_stream		



# tokenSeq = convert_int_to_sequence(note_seqs[0], decoder)
# stream = sequence_to_notes(tokenSeq, sample_rate)
# f = stream.write('midi', fp='testoutput.midi')
# stream.show('midi')