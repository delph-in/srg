import sys
import string
import glob
import subprocess
import json
from tempfile import NamedTemporaryFile
from delphin import itsdb
from srg_freeling2yy import convert_sentences
# I cannot figure out how to use the pyfreeling library:
from freeling.freeling_API.tokenize_and_tag import Freeling_tok_tagger

# REMOVE = {'The tobacco garden dog barked.', 'Abrams wiped the table clean.',
#           'Abrams left it to Browne to bark.', 'How happy was Abrams?'}

def read_testsuite2(ts):
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

def read_testsuite(ts):
    items = ts['item']
    # Strip the trailing hyphens to match old LKB output, although may want to put them back in later.
    return [item['i-input'].strip('-') for item in items ]
    # debug:
    #sentences = sentences[47:49]

def run_script_json(script_path, arg_path):
    output = subprocess.run("'%s' '%s'" % (script_path, str(arg_path)),shell=True,stdout=subprocess.PIPE)
    #print(output.stdout.decode('utf-8'))
    decoded_output = output.stdout.decode('utf-8')
    json_strs = parse_recursive_dicts(decoded_output)
    return json_strs
    #return json.loads(decoded_output)

def run_script(script_path, arg_path):
    output = subprocess.run("'%s' '%s'" % (script_path, str(arg_path)),shell=True,stdout=subprocess.PIPE)
    #print(output.stdout.decode('utf-8'))
    decoded_output = output.stdout.decode('utf-8')
    return [ ln_set for ln_set in decoded_output.split('\n\n') if ln_set ]

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
    ftt = Freeling_tok_tagger()
    sentence_list = read_testsuite(ts)
    output = ftt.tokenize_and_tag(sentence_list)
    yy = convert_sentences(output)
    assert len(yy) == len(ts['item'])
    print('{} items in the corpus'.format(len(yy)))
    for i, row in enumerate(ts['item']):
        ts['item'].update(i, {'i-tokens': yy[i]})
        if ts['item'][i]['i-id'] == 10:
            ts['item'].update(i, {'i-id':101})
    ts.commit()

'''
I cannot figure out how to pass the subprocess anything that is not a file.
Furthermore, the freeling command which is currently the only one I can successfully use,
analyze -f es.cfg --output json
outputs a string which is a concatenation of json dicts, where begin and end of each token
are computed from the beginning of the first sentence, as if the whole output were a single sentence (?).
So, for now I am left with creating a temporary file for each input sentence.
I will try to ask L. Padro about it (or yet find the answer in the docs).
'''
def freeling2json(s):
    tmp_sentence_file = NamedTemporaryFile("w", delete=False)
    with open(tmp_sentence_file.name, 'w') as tmp_f:
        if not s[-1] in string.punctuation:
            # assume a dot at the end
            s = s + '.'
        tmp_f.write(s + '\n')
    scr_out_json = run_script('./sentences2freeling.sh', tmp_f.name)
    return scr_out_json


if __name__ == "__main__":
    for i, ts_path in enumerate(sorted(glob.iglob(sys.argv[1] + '/**'))):
        ts = itsdb.TestSuite(ts_path)
        print('Processing {}'.format(ts.path.stem))
        update_testsuite(ts)