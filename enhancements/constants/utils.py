def annotate(labels_map):
    return [
        (item.value, description)
        for item, description in labels_map.items()
    ]
