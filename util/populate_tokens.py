import sys
import string
import glob
import subprocess
from tempfile import NamedTemporaryFile
from delphin import itsdb
from srg_freeling2yy import convert_sentences

def read_testsuite(ts):
    items = ts['item']
    sentences = [item['i-input'] for item in items]
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
    return [s for s in output.stdout.decode('utf-8').split('\n\n') if s]

def update_testsuite(ts):
    sentence_list = read_testsuite(ts)
    script_output = run_script('./sentences2freeling.sh', sentence_list)
    yy = convert_sentences(script_output)
    assert len(yy) == len(ts['item'])
    for i, row in enumerate(ts['item']):
        ts['item'].update(i, {'i-tokens': yy[i]})
    ts.commit()


if __name__ == "__main__":
    print(5)
    for i, ts_path in enumerate(sorted(glob.iglob(sys.argv[1] + '/**'))):
        ts = itsdb.TestSuite(ts_path)
        update_testsuite(ts)