def build_convert_dict(max_note, instruments, sample_rate):
    convert_keys = []
    for instrument in instruments:
        convert_keys.extend([instrument + str(note) for note in range(max_note + 1)])
        convert_keys.extend(["end" + instrument + str(note) for note in range(max_note + 1)])
    convert_keys.extend(["wait" + str(tick) for tick in range(1, 2 * sample_rate + 1)])
    convert_dict = dict((action, encoding) for encoding, action in enumerate(convert_keys))
    return convert_dict, convert_keys