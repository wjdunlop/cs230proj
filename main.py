import numpy as np

import datacollector

def build_convert_dict(max_note, instruments, sample_rate):
    convert_keys = []
    for instrument in instruments:
        convert_keys.extend([instrument + str(note) for note in range(max_note + 1)])
        convert_keys.extend(["end" + instrument + str(note) for note in range(max_note + 1)])
    convert_keys.extend(["wait" + str(tick) for tick in range(1, 2 * sample_rate + 1)])
    convert_dict = dict((action, encoding) for encoding, action in enumerate(convert_keys))
    return convert_dict

def main():
    max_note = 127
    instruments = ['t']
    sample_rate = 12
    converter = build_convert_dict(max_note, instruments, sample_rate)
    datacollector.collect_solo_songs(converter, max_note, len(instruments), sample_rate)

if __name__ == "__main__":
    main()