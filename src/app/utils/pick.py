def pick(input_dict, keys):
    return {key: input_dict[key] for key in keys if key in input_dict}
