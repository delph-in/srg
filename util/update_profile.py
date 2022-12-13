
def find_all(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def insert_at(filepath, position):
    with open(filepath, 'r') as f:
        items = f.readlines()
    updated = []
    for item in items:
        indices = find_all(item,'@')
        assert len(indices) >= position
        updated.append(item[:indices[position-1]]+'@'+ item[indices[position-1]:])
    with open(filepath+'updated', 'w') as f:
        for updated_item in updated:
            f.write(updated_item)


insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/run',4)