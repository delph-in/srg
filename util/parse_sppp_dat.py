
def parse_sppp(filepath):
    # Dictionaries to return:
    fuse = {}
    replace = {}
    no_disambiguate = {}
    output = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for i,ln in enumerate(lines):
        if not ln.startswith('#'):
            if ln.strip() == '<NoDisambiguate>':
                pass
            elif ln.strip() == '<ReplaceAll>':
                pass
            elif ln.strip() == '<Fusion>':
                end_fusion = find_concluding_line(lines, i, '<Fusion>')
                fuse = parse_fusion(lines[i+1:end_fusion])
            elif ln.strip() == '<Output>':
                pass
    return fuse, replace, no_disambiguate, output

def find_concluding_line(lines, start, opening):
    closing = '</' + opening[1:]
    for i in range(start, len(lines)):
        if lines[i].strip() == closing:
            return i
    return None

def parse_fusion(lines):
    fuse = {}
    for ln in lines:
        tag1, tag2, arrow, fused_tag = ln.strip().split()
        fuse[tag1 + '" "+' + tag2] = fused_tag
    return fuse