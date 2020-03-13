import datacollector
import evaluate
import generate
import train
import utils

import numpy as np
from sklearn.model_selection import train_test_split

def main():
    # dataset hyperparams
    sequence_length = 50
    augment_dataset = False

    # uncomment the below for dataset collection
    max_note = 127
    instruments = ['t']
    sample_rate = 12
    encoding_size = len(instruments) * (max_note + 1) * 2 + (sample_rate * 2)
    num_notes = len(instruments) * (max_note + 1)
    encoder, decoder = utils.build_convert_dict(max_note, instruments, sample_rate)
    X, y = datacollector.collect_solo_songs(encoder, max_note, len(instruments), sample_rate, sequence_length,
                                            augment_dataset)
    X_t, X_test, y_t, y_test = train_test_split(X, y, test_size=0.02, random_state=49)
    X_train, X_val, y_train, y_val = train_test_split(X_t, y_t, test_size=0.02, random_state=7)
    print(X.shape, X_t.shape, X_test.shape, X_train.shape, X_val.shape)


    # uncomment the below for training
    # train.train(X_train, y_train, encoding_size)

    # uncomment the below for evaluation
    evaluate.evaluate(X_train, y_train, X_val, y_val, X_test, y_test, encoding_size, 'weights.02-2.2507.hdf5')

    # uncomment the below for generation
    encoded_notes = generate.generate(X, 100, 'weights.19-1.0584.hdf5', encoding_size, num_notes)
    print(encoded_notes)
    outputs_tokens = generate.convert_int_to_sequence(encoded_notes, decoder)
    print(outputs_tokens)
    outputs_notes = generate.sequence_to_notes(outputs_tokens, sample_rate)

    outputs_notes.write('midi', fp='testoutput10epochscase1.midi')
	
if __name__ == "__main__":
    main()