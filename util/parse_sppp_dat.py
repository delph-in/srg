
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
                end_nodiambiguate = find_concluding_line(lines, i, '<NoDisambiguate>')
                no_disambiguate = parse_nodisambiguate(lines[i+1:end_nodiambiguate])
            elif ln.strip() == '<ReplaceAll>':
                end_replace = find_concluding_line(lines, i, '<ReplaceAll>')
                replace = parse_replace(lines[i+1:end_replace])
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

def parse_nodisambiguate(lines):
    nodisambiguate = {}
    for ln in lines:
        word, position = ln.strip().split()
        nodisambiguate[word] = position
    return nodisambiguate

def parse_fusion(lines):
    fuse = {}
    for ln in lines:
        #tags_to_fuse, fused_tag = ln.strip().split('=>')
        tag1, tag2, arrow, fused_tag = ln.strip().split()
        fuse[tag1 + '" "+' + tag2] = fused_tag
        #fuse[tags_to_fuse.strip()] = fused_tag
    return fuse

def parse_replace(lines):
    replace = {}
    for ln in lines:
        if ln.strip():
            # the line is of the form: <surfaceform> <lemma1> <tag1> <lemma2> <tag2> ...
            # split the line on the first space:
            form, lemma_tag_pairs = ln.strip().split(' ', 1)
            # split the lemma-tag pairs on spaces:
            lemma_tag_pairs = lemma_tag_pairs.split()
            # put the odd items in lemma_tag_pairs list into the 'tag' key of replace[form] and the even items into the 'lemma' key:
            replace[form] = {'tag': lemma_tag_pairs[1::2], 'lemma': lemma_tag_pairs[::2]}
    return replace