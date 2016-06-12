def annotate(labels_map):
    return sorted([
        (item, description)
        for item, description in labels_map.items()
    ])
