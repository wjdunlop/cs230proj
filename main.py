import datacollector
import generate
import train
import utils

def main():
    max_note = 127
    instruments = ['t']
    sample_rate = 12
    encoding_size = len(instruments) * (max_note + 1) * 2 + (sample_rate * 2)
    num_notes = len(instruments) * (max_note + 1)
    encoder, decoder = utils.build_convert_dict(max_note, instruments, sample_rate)
    X, y = datacollector.collect_solo_songs(encoder, max_note, len(instruments), sample_rate)

    # uncomment the below for training
    # train.train(X, y, encoding_size)

    # uncomment the below for generation
    encoded_notes = generate.generate(X, 100, 'weights.02-2.2507.hdf5', encoding_size, num_notes)

if __name__ == "__main__":
    main()