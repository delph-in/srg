
def find_all(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def insert_at(filepath, positions):
    with open(filepath, 'r') as f:
        items = f.readlines()
    updated = []
    for item in items:
        updated_item = item
        for i,pos in enumerate(positions):
            indices = find_all(updated_item,'@')
            assert len(indices) >= pos+i
            updated_item = updated_item[:indices[pos-1+i]]+'@'+ updated_item[indices[pos-1+i]:]
        updated.append(updated_item)
    with open(filepath+'updated', 'w') as f:
        for updated_item in updated:
            f.write(updated_item)


insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/run',[4])
insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/parse',[24,24,24,24,24])
insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/edge',[8])
insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/score',[3,3,3,3])
insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/item',[8,8,8])