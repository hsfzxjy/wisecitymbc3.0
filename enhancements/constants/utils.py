def annotate(labels_map):
    return sorted([
        (item.value, description)
        for item, description in labels_map.items()
    ])
