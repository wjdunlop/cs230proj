# cs230proj
Project for Stanford CS 230 - Deep Learning
Turned in: March 17, 2020

While music generation is a relatively well-explored field of deep learning, most generators are limited to generating notes of static length and timing for the piano strictly. In order to build a more compelling and robust music generation model, we divide our task into two main segments: music classification and music generation. Despite limited time to accomplish the latter, we reached interesting results from a musical standpoint, and in doing so managed to build a LSTM-based RNN that is quite effective at predicting the next note in sequences of trumpet soloist music.

We curated our own dataset of just under 2,000 trumpet melodies from www.8notes.com, gathering their freely available MIDI files for trumpet. We optionally augment this data by transposing it to all other keys. For training sequences of length 10, we extracted 933,102 examples from this data.

Our feature vectors are composed of a series of encoded tokens of varying length, where this varying length is given by the sequence length hyperparameter. This hyperparameter was tested at length 10 and at length 50. Each of the MIDI files listed above is converted into a sequence of string tokens, such as “t88” (which represents starting to play note 88 on the trumpet), “endt88” (which represents halting a note 88 being played on the trumpet), and “wait12” (which means to wait for 12 ticks). These string tokens are then converted via a dictionary to integer values, where note beginnings are towards the start, note endings are towards the middle, and wait periods are towards the end. Outputs are converted in the same manner.

We found that our model was able to generate music respecting physical limitations of the trumpet: without large intervals, and in an acceptable range. The model eventually learned rests and complex rhythms. The complexity increased rapidly. See /examples/ and listen to the .midi files!


