def diff(dict1, dict2):
    """Calculate the differences between two dicts.

    Arguments:
        dict1 {dict} The main dict.
        dict2 {dict}
    """

    differences = []

    for key, value in dict1.items():
        if value != dict2.get(key):
            differences.append(key)

    return differences
