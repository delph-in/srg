#! /usr/bin/python3

from freeling.freeling_API import pyfreeling
import sys, os, string

class Freeling_tok_tagger:
    def __init__(self):
        os.environ["FREELINGDIR"] = '/usr'
        if not os.path.exists(os.environ["FREELINGDIR"]+"/share/freeling") :
           print("Folder",os.environ["FREELINGDIR"]+"/share/freeling",
                 "not found.\nPlease set FREELINGDIR environment variable to FreeLing installation directory",
                 file=sys.stderr)
           sys.exit(1)

        # Location of FreeLing configuration files.
        self.DATA = os.environ["FREELINGDIR"]+"/share/freeling/"
        # Init locales
        pyfreeling.util_init_locale("default")
        # create language detector. Used just to show it. Results are printed
        # but ignored (after, it is assumed language is LANG)
        self.la=pyfreeling.lang_ident(self.DATA+"common/lang_ident/ident-few.dat")
        # create options set for maco analyzer. Default values are Ok, except for data files.
        self.LANG="es"
        self.op= pyfreeling.maco_options(self.LANG)
        self.op.set_data_files( "",
                           self.DATA + "common/punct.dat",
                           self.DATA + self.LANG + "/dicc.src",
                           self.DATA + self.LANG + "/afixos.dat",
                           "",
                           self.DATA + self.LANG + "/locucions.dat",
                           self.DATA + self.LANG + "/np.dat",
                           self.DATA + self.LANG + "/quantities.dat",
                           self.DATA + self.LANG + "/probabilitats.dat")

        # create analyzers
        self.tk=pyfreeling.tokenizer(self.DATA+self.LANG+"/tokenizer.dat")
        self.sp=pyfreeling.splitter(self.DATA+self.LANG+"/splitter.dat")
        self.mf=pyfreeling.maco(self.op)

        # activate mmorpho odules to be used in next call
        self.mf.set_active_options(umap=False, num=True, pun=True, dat=False,  # select which among created
                              dic=True, aff=True, comp=False, rtk=True,  # submodules are to be used.
                              mw=False, ner=True, qt=False, prb=True )  # default: all created submodules are used

        self.tg=pyfreeling.hmm_tagger(self.DATA+self.LANG+"/tagger.dat",True,1)
        #self.tg = pyfreeling.relax_tagger(self.DATA+self.LANG+"/constr_gram-B.dat",500,670.0,0.001,True,1)

    def tokenize_and_tag(self, sentence_list):
        output = []
        sid=self.sp.open_session()
        # process input text
        for i,lin in enumerate(sentence_list):
            fake_final_dot = False
            if (not lin[-1] in string.punctuation) or lin.endswith('...'):
                # assume a dot at the end since otherwise Freeling sometimes can't handle the sentence
                lin = lin + ' .'
                fake_final_dot = True
            output.append({'sentence': lin, 'tokens':[]})
            # For now, do not assume that uppercased items are all named entities.
            # This may need to change in the future because maybe the user need to take care of lowercasing things.
            s = self.tk.tokenize(lin.lower().capitalize()) if lin.isupper() else self.tk.tokenize(lin)
            s = self.sp.split(sid,s,False)
            s = self.mf.analyze(s)
            s = self.tg.analyze(s)
            if len(s) == 0:
                print("No Freeling analysis for {}".format(lin))
                output[i]['sentence'] = lin
                output[i]['tokens'] = None
            else:
                assert len(s) == 1
                s = s[0]
                ws = s.get_words()
                if fake_final_dot:
                    ws = ws[:-1]
                for j,w in enumerate(ws) :
                    output[i]['tokens'].append({'lemma':w.get_lemma(), 'form': w.get_form(),
                                                'start':w.get_span_start(), 'end': w.get_span_finish(),
                                                'selected-tag': w.get_tag(), 'all-tags': []})
                    analyses = list(w.get_analysis())
                    for a in analyses:
                        #print("\ttag: {}, prob: {}".format(a_i.get_tag(), a_i.get_prob()))
                        output[i]['tokens'][j]['all-tags'].append({'tag': a.get_tag(), 'prob': a.get_prob()})
                        if a.get_tag() == output[i]['tokens'][j]['selected-tag']:
                            output[i]['tokens'][j]['selected-prob'] = a.get_prob()
        # clean up
        self.sp.close_session(sid)
        return output
    
