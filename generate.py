import numpy as np

import train

def generate(X, gen_length, weights_name, encoding_size, num_notes):
    model = train.get_model(X, encoding_size)
    model.load_weights(weights_name)

    initial_seq_idx = np.random.randint(X.shape[0])
    sequence = X[initial_seq_idx]

    sequence = sequence.reshape(1, sequence.shape[0], sequence.shape[1])
    for i in range(gen_length):
        prediction = model.predict(sequence)
        new_elem = np.argmax(prediction)
        sequence[:, 0:sequence.shape[1] - 1, :] = sequence[:, 1:, :]
        sequence[:, sequence.shape[1] - 1, :] = new_elem
    return sequence
