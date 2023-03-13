import sys
import string
import glob
import subprocess
import json
from tempfile import NamedTemporaryFile
from delphin import itsdb
from srg_freeling2yy import convert_sentences_json
# I cannot figure out how to use the pyfreeling library:
# from pyfreeling import Analyzer

# REMOVE = {'The tobacco garden dog barked.', 'Abrams wiped the table clean.',
#           'Abrams left it to Browne to bark.', 'How happy was Abrams?'}

def read_testsuite(ts):
    items = ts['item']
    # Strip the trailing hyphens to match old LKB output, although may want to put them back in later.
    sentences = [item['i-input'].strip('-') for item in items ]
    # debug:
    #sentences = sentences[47:49]
    tmp_sentence_file = NamedTemporaryFile("w", delete=False)
    with open(tmp_sentence_file.name, 'w') as tmp_f:
        for s in sentences:
            if not s[-1] in string.punctuation:
                # assume a dot at the end
                s = s + '.'
            tmp_f.write(s+'\n')
    return tmp_f.name

def run_script(script_path, arg_path):
    output = subprocess.run("'%s' '%s'" % (script_path, str(arg_path)),shell=True,stdout=subprocess.PIPE)
    #print(output.stdout.decode('utf-8'))
    decoded_output = output.stdout.decode('utf-8')
    json_strs = parse_recursive_dicts(decoded_output)
    return json_strs

'''
Code produced by 
ChatGPT
'''
def parse_recursive_dicts(input_string):
    sentences = []
    start = 0
    end = 0

    while True:
        start = input_string.find('{', end)
        if start == -1:
            break
        #print(input_string[start],end='')
        end = start + 1
        depth = 1
        while depth > 0:
            #print(input_string[end],end='')
            if input_string[end] == '{':
                depth += 1
            elif input_string[end] == '}':
                depth -= 1
            end += 1
        sentence_str = input_string[start:end]
        sentence = json.loads(sentence_str)
        sentences.append(sentence)
        #print('\n')
    return sentences

def update_testsuite(ts):
    # analyzer = pyfreeling.Analyzer()
    # analyzer.lang = 'es'
    # analyzer.config = 'es.cfg'
    #scr_out_xml = analyzer.run(sentence_list)
    sentence_list = read_testsuite(ts)
    scr_out_json = run_script('./sentences2freeling.sh', sentence_list)
    yy = convert_sentences_json(scr_out_json)
    assert len(yy) == len(ts['item'])
    print('{} items in the corpus'.format(len(yy)))
    for i, row in enumerate(ts['item']):
        ts['item'].update(i, {'i-tokens': yy[i]})
        if ts['item'][i]['i-id'] == 10:
            ts['item'].update(i, {'i-id':101})
    ts.commit()


if __name__ == "__main__":
    for i, ts_path in enumerate(sorted(glob.iglob(sys.argv[1] + '/**'))):
        ts = itsdb.TestSuite(ts_path)
        print('Processing {}'.format(ts.path.stem))
        update_testsuite(ts)