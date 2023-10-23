def omit(input_dict, keys_to_omit):
    return {key: input_dict[key] for key in input_dict if key not in keys_to_omit}
