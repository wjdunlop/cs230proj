import datacollector
import train
import utils

def main():
    max_note = 127
    instruments = ['t']
    sample_rate = 12
    encoding_size = len(instruments) * (max_note + 1) * 2 + (sample_rate * 2)
    encoder, decoder = utils.build_convert_dict(max_note, instruments, sample_rate)
    X, y = datacollector.collect_solo_songs(encoder, max_note, len(instruments), sample_rate)
    train.train(X, y, encoding_size)

if __name__ == "__main__":
    main()