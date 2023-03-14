#! /usr/bin/python3

import pyfreeling
import sys, os

## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------

os.environ["FREELINGDIR"] = '/usr'

if not os.path.exists(os.environ["FREELINGDIR"]+"/share/freeling") :
   print("Folder",os.environ["FREELINGDIR"]+"/share/freeling",
         "not found.\nPlease set FREELINGDIR environment variable to FreeLing installation directory",
         file=sys.stderr)
   sys.exit(1)


# Location of FreeLing configuration files.
DATA = os.environ["FREELINGDIR"]+"/share/freeling/"
# Init locales
pyfreeling.util_init_locale("default")
# create language detector. Used just to show it. Results are printed
# but ignored (after, it is assumed language is LANG)
la=pyfreeling.lang_ident(DATA+"common/lang_ident/ident-few.dat")
# create options set for maco analyzer. Default values are Ok, except for data files.
LANG="es"
op= pyfreeling.maco_options(LANG)
op.set_data_files( "", 
                   DATA + "common/punct.dat",
                   DATA + LANG + "/dicc.src",
                   DATA + LANG + "/afixos.dat",
                   "",
                   DATA + LANG + "/locucions.dat", 
                   DATA + LANG + "/np.dat",
                   DATA + LANG + "/quantities.dat",
                   DATA + LANG + "/probabilitats.dat")

# create analyzers
tk=pyfreeling.tokenizer(DATA+LANG+"/tokenizer.dat")
sp=pyfreeling.splitter(DATA+LANG+"/splitter.dat")
mf=pyfreeling.maco(op)

# activate mmorpho odules to be used in next call
mf.set_active_options(False, True, True, True,  # select which among created 
                      True, True, False, True,  # submodules are to be used. 
                      True, True, True, True )  # default: all created submodules are used

# create tagger, sense anotator, and parsers
tg=pyfreeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2)
#sen=pyfreeling.senses(DATA+LANG+"/senses.dat");
#parser= pyfreeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
#dep=pyfreeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol());

sid=sp.open_session()
# process input text
#lin=sys.stdin.readline();
lin = "El perro del pueblo duerme."

l = tk.tokenize(lin)
ls = sp.split(sid,l,False)

ls = mf.analyze(ls)
ls = tg.analyze(ls)

## output results
for s in ls :
    print(s)
    ws = s.get_words()
    for w in ws :
       print("FORM: {} LEMMA: {} START: {} END: {}".format(w.get_form(), w.get_lemma(),
                                                           w.get_span_start(), w.get_span_finish()))
       analyses = list(w.get_analysis())
       for a_i in analyses:
           print("\ttag: {}, prob: {}".format(a_i.get_tag(), a_i.get_prob()))

# clean up       
sp.close_session(sid)
    
