from Assets import Assets

assets = Assets()
path_to_file = 'data/tikets.properties'


def load_properties(sep='=', comment_char='#'):
    props = {}
    with open(path_to_file, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    assets.old_to_new_tiket = props

