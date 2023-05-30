#! /usr/bin/python3

from freeling_api.python_API import pyfreeling_api
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
        self.CUSTOM_DATA = "/home/olga/delphin/SRG/grammar/srg/util/freeling_api/srg-freeling-debug.dat"
        # Init locales
        pyfreeling_api.util_init_locale("default")
        # create language detector. Used just to show it. Results are printed
        # but ignored (after, it is assumed language is LANG)
        self.la=pyfreeling_api.lang_ident(self.DATA+"common/lang_ident/ident-few.dat")
        # create options set for maco analyzer. Default values are Ok, except for data files.
        self.LANG="es"
        self.op= pyfreeling_api.maco_options(self.LANG)
        self.op.set_data_files( self.CUSTOM_DATA,
                           self.DATA + "common/punct.dat",
                           self.DATA + self.LANG + "/dicc.src",
                           self.DATA + self.LANG + "/afixos.dat",
                           "",
                           self.DATA + self.LANG + "/locucions.dat",
                           self.DATA + self.LANG + "/nerc/nerc/nerc.dat",
                           self.DATA + self.LANG + "/quantities.dat",
                           self.DATA + self.LANG + "/probabilitats.dat")

        # create analyzers
        self.tk=pyfreeling_api.tokenizer(self.DATA+self.LANG+"/tokenizer.dat")
        self.sp=pyfreeling_api.splitter(self.DATA+self.LANG+"/splitter.dat")
        self.mf=pyfreeling_api.maco(self.op)

        # activate mmorpho odules to be used in next call
        self.mf.set_active_options(umap=True, num=True, pun=True, dat=False,  # select which among created
                              dic=True, aff=True, comp=False, rtk=True,  # submodules are to be used.
                              mw=True, ner=True, qt=False, prb=True )  # default: all created submodules are used

        self.tg=pyfreeling_api.hmm_tagger(self.DATA+self.LANG+"/tagger.dat",False,0)
        #self.tg = pyfreeling_api.relax_tagger(self.DATA+self.LANG+"/constr_gram-B.dat",500,670.0,0.001,True,1)

    def tokenize_and_tag(self, sentence_list):
        output = []
        sid=self.sp.open_session()
        # process input text
        for i,lin in enumerate(sentence_list):
            output.append({'sentence': lin, 'tokens':[]})
            #if "aburrido" in lin:
            #    print("debug")
            # With the basic NER Freeling module, may need this, as it will assume that
            # all uppercased items are all named entities.
            #s = self.tk.tokenize(lin.lower().capitalize()) if lin.isupper() else self.tk.tokenize(lin)
            s = self.freeling_analyze(lin, sid)
            if len(s) == 0 or len(s) > 1:
                if len(s) == 0:
                    print("No Freeling analysis for {}".format(lin))
                else:
                    print("Line {} seems to contain more than one sentence and was not tokenized properly. Skipping it.".format(lin))
                output[i]['sentence'] = lin
                output[i]['tokens'] = None
            else:
                s = s[0]
                ws = s.get_words()
                for j,w in enumerate(ws) :
                    tags_probs = self.get_selected_tags(w)
                    tag = '" "+'.join([tp['tag'] for tp in tags_probs])
                    prob = tags_probs[-1]['prob']
                    #print("lemma: {}, form: {}, start: {}, end: {}, tag: {}".format(w.get_lemma(), w.get_form(), w.get_span_start(), w.get_span_finish(), w.get_tag()))
                    output[i]['tokens'].append({'lemma':w.get_lemma(), 'form': w.get_form(),
                                                'start':w.get_span_start(), 'end': w.get_span_finish(),
                                                'selected-tag': tag, 'selected-prob': prob})
        # clean up
        self.sp.close_session(sid)
        return output

    def freeling_analyze(self, lin, sid):
        s = self.tk.tokenize(lin)
        s = self.sp.split(sid, s, True)
        s = self.mf.analyze(s)
        s = self.tg.analyze(s)
        return s

    def get_selected_tags(self, w):
        tags = []
        for a in w:
            if a.is_selected():
                if a.is_retokenizable():
                    tks = a.get_retokenizable()
                    for tk in tks:
                        tags.append(({'tag': tk.get_tag(), 'prob': a.get_prob()}))
                else:
                    tags.append(({'tag': a.get_tag(), 'prob': a.get_prob()}))
            #else:
            #    print("Non-selected analysis: {}".format(a.get_tag()))
        return tags
