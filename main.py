import datacollector
import evaluate
import generate
import train
import utils
import pickle

import numpy as np
from sklearn.model_selection import train_test_split

def main():
    print("SEQ 50 CNT")
    
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
    # X, y = datacollector.collect_solo_songs(encoder, max_note, len(instruments), sample_rate, sequence_length,
    #                                         augment_dataset)

    X = pickle.load(open("x.pickle", "rb"))
    y = pickle.load(open('y.pickle', 'rb'))
    # pickle.dump(X, pickle_x)
    # pickle_x.close()
    # pickle.dump(y, pickle_y)
    # pickle_y.close()

    X_t, X_test, y_t, y_test = train_test_split(X, y, test_size=0.02, random_state=49)
    X_train, X_val, y_train, y_val = train_test_split(X_t, y_t, test_size=0.02, random_state=7)
    print(X.shape, X_t.shape, X_test.shape, X_train.shape, X_val.shape)


    # # uncomment the below for training
   
    # train.train(X_train, y_train, encoding_size)

    # # uncomment the below for evaluation

    weights_name = 'weights.49-0.8625.hdf5'
    # evaluate.evaluate(X_train, y_train, X_val, y_val, X_test, y_test, encoding_size, weights_name)
    print("SEQ 10 noAUG Forward!")
    # model = train.get_model(X_test, encoding_size)
    # model.load_weights(weights_name)
    # print('weights loaded')
    # y_pred = model.predict(X_test)
    # y_pred = y_test
    # print(y_test)
    # # print(y_pred)
    # print(y_test)
    # print(y_test.shape)
    # # print(type(y_test))
    # print(y_pred)
    # print(y_pred.shape)
    # # print(type(y_pred))
    # a = y_pred.argmax(axis = 1)
    # print(a)
    # y_pred_hardmax = np.zeros(y_pred.shape)
    # y_pred_hardmax[np.arange(a.shape[0]),a] = 1
    # print(y_pred_hardmax)
    # print(list(y_test.argmax(axis=0)))
    # print(list(y_pred_hardmax.argmax(axis=0)))
    # evaluate.plot_confusion_matrix('confusion_matrix.png', y_test.argmax(axis=1), y_pred_hardmax.argmax(axis=1))

    # uncomment the below for generation
    for i in range(1, 20):
        encoded_notes = generate.generate(X, 500, 'weights.49-0.8625.hdf5', encoding_size, num_notes)
        print(encoded_notes)
        outputs_tokens = generate.convert_int_to_sequence(encoded_notes, decoder)
        print(outputs_tokens)
        outputs_notes = generate.sequence_to_notes(outputs_tokens, sample_rate)

        outputs_notes.write('midi', fp='CHECK_'+str(i)+'.midi')
	
if __name__ == "__main__":
    main()