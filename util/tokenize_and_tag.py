#! /usr/bin/python3

from freeling_api.python_API import pyfreeling_api
import sys, os

PATH_TO_SPPP_DAT = '/home/olga/delphin/SRG/grammar/srg/util/freeling_api/srg-freeling.dat'

class Freeling_tok_tagger:
    '''
    NB: There are numerous ways to configure the Freeling modules (the morphological analyzer, the splitter, the tagger).
    Each small difference may result in the grammar no longer parsing things or parsing them differently,
    because some of the tags will be different, and the tokenization may be different.
    In principle, all the possibilities are described well in the Freeling docs: https://freeling-tutorial.readthedocs.io/
    but they are vast and it is not always trivial to find the relevant pieces.
    '''
    def __init__(self):
        os.environ["FREELINGDIR"] = '/usr'
        if not os.path.exists(os.environ["FREELINGDIR"]+"/share/freeling") :
           print("Folder",os.environ["FREELINGDIR"]+"/share/freeling",
                 "not found.\nPlease set FREELINGDIR environment variable to FreeLing installation directory",
                 file=sys.stderr)
           sys.exit(1)

        # Location of FreeLing configuration files.
        self.DATA = os.environ["FREELINGDIR"]+"/share/freeling/" #usermap; currently empty
        self.CUSTOM_DATA = PATH_TO_SPPP_DAT
        # Init locales
        pyfreeling_api.util_init_locale("default")
        # create language detector. Used just to show it. Results are printed
        # but ignored (after, it is assumed language is LANG)
        self.la=pyfreeling_api.lang_ident(self.DATA+"common/lang_ident/ident-few.dat")
        # create options set for maco analyzer. Default values are Ok, except for data files.
        self.LANG="es" # This means the file es.cfg will be used (located in the freeling installation location)
        self.op= pyfreeling_api.maco_options(self.LANG)
        self.op.set_data_files( self.CUSTOM_DATA,
                           self.DATA + "common/punct.dat",
                           self.DATA + self.LANG + "/dicc.src",
                           self.DATA + self.LANG + "/afixos.dat", # important for the clitics!
                           "",
                           self.DATA + self.LANG + "/locucions.dat",
                           self.DATA + self.LANG + "/nerc/nerc/nerc.dat",
                           self.DATA + self.LANG + "/quantities.dat",
                           self.DATA + self.LANG + "/probabilitats.dat")

        # create analyzers
        self.tk=pyfreeling_api.tokenizer(self.DATA+self.LANG+"/tokenizer.dat")
        self.tk_rtk = pyfreeling_api.tokenizer(self.DATA + self.LANG + "/tokenizer.dat")
        self.sp=pyfreeling_api.splitter(self.DATA+self.LANG+"/splitter.dat")
        self.mf=pyfreeling_api.maco(self.op)
        self.mf_alt= pyfreeling_api.maco(self.op)

        # activate mmorpho odules to be used in next call
        # These are crucial for the specific output.
        self.mf.set_active_options(umap=True, num=True, pun=True, dat=False,  # no time and date detection (dat=False)
                              dic=True, aff=True, comp=False, rtk=True,
                              mw=True, ner=True, qt=False, prb=True )  # No quantities detection (qt=False)

        # Alternative freeling setup with no multiword detection
        self.mf_alt.set_active_options(umap=True, num=True, pun=True, dat=False,  # no time and date detection (dat=False)
                                   dic=True, aff=True, comp=False, rtk=True,
                                   mw=False, ner=True, qt=False, prb=True)  # No quantities detection (qt=False)

        # The tagger is instantiated with RETOKENIZATION SET TO FALSE (second parameter). This is crucial to get
        # sequences of tags such as VMN00000 +PP3MSA0, for words like "creerlo" which will not be tokenized into two
        self.tg=pyfreeling_api.hmm_tagger(self.DATA+self.LANG+"/tagger.dat",False,0)
        self.tg_rtk = pyfreeling_api.hmm_tagger(self.DATA + self.LANG + "/tagger.dat", True, 1)

    def tokenize_and_tag(self, sentence_list, override_dicts):
        output = []
        sid=self.sp.open_session()
        # process input text
        for i,lin in enumerate(sentence_list):
            sys.stderr.write("{}/{} sentences processed\r".format(i+1, len(sentence_list)))
            sys.stderr.flush()
            output.append({'sentence': lin, 'tokens':[]})
            #if "no sólo es" in lin:
            #    print("debug")
            # With the basic NER Freeling module, may need this, as it will assume that
            # all uppercased items are all named entities.
            #s = self.tk.tokenize(lin.lower().capitalize()) if lin.isupper() else self.tk.tokenize(lin)
            s = self.freeling_analyze(lin, sid)
            if len(s) == 0 or len(s) > 1:
                if len(s) == 0:
                    print("No Freeling analysis for {}".format(lin),file=sys.stderr)
                else:
                    print("Line {} seems to contain more than one sentence and was not tokenized properly. Skipping it.".format(lin),file=sys.stderr)
                print("",file=sys.stderr)
                sys.stderr.flush()
                output[i]['sentence'] = lin
                output[i]['tokens'] = None
            else:
                s = s[0]
                ws = s.get_words()
                for j,w in enumerate(ws) :
                    tags_probs, additional_arcs = self.get_selected_tags(w, override_dicts)
                    additional = len(additional_arcs) > 0
                    tag = '" "+'.join([tp['tag'] for tp in tags_probs])
                    prob = tags_probs[-1]['prob']
                    #print("lemma: {}, form: {}, start: {}, end: {}, tag: {}".format(w.get_lemma(), w.get_form(), w.get_span_start(), w.get_span_finish(), w.get_tag()))
                    output[i]['tokens'].append({'lemma':w.get_lemma(), 'form': w.get_form(),
                                                'start':w.get_span_start(), 'end': w.get_span_finish(),
                                                'tag': tag, 'prob': prob, 'additional': additional})
                    for k,arc in enumerate(additional_arcs):
                        entry = {'lemma': arc['lemma'], 'form': w.get_form(),
                                                    'start': w.get_span_start(), 'end': w.get_span_finish(),
                                                    'tag': arc['tag'], 'prob': prob, 'additional': True}
                        if k == len(additional_arcs) - 1:
                            entry['last'] = True
                        output[i]['tokens'].append(entry)
        # clean up
        print("", file=sys.stderr)
        sys.stderr.flush()
        self.sp.close_session(sid)
        return output

    def freeling_analyze(self, lin, sid):
        #print(lin)
        if not 'por qué' in lin.lower():
            s = self.tk.tokenize(lin)
        else:
            s = self.tk_rtk.tokenize(lin)
        s = self.sp.split(sid, s, True)
        s = self.mf.analyze(s)
        s = self.tg.analyze(s)
        return s

    def get_selected_tags(self, w, override_dicts):
        tags = []
        additional_arcs = []
        for a in w:
            if a.is_selected():
                if a.is_retokenizable():
                    tks = a.get_retokenizable()
                    for tk in tks:
                        tags.append(({'tag': tk.get_tag(), 'prob': a.get_prob()}))
                else:
                    if not w.get_form().lower() in override_dicts['replace']:
                        tags.append(({'additional':False, 'tag': a.get_tag(), 'prob': a.get_prob()}))
                    else:
                        for i, additional_tag in enumerate(override_dicts['replace'][w.get_form().lower()]['tag']):
                            additional_lemma = override_dicts['replace'][w.get_form().lower()]['lemma'][i]
                            if i == 0:
                                tags.append(({'additional':True, 'tag': additional_tag, 'prob': -1, 'lemma': additional_lemma}))
                            else:
                                additional_arcs.append(({'additional':True, 'tag': additional_tag, 'prob': -1, 'lemma': additional_lemma}))
            else:
                # There are words for which Freeling selected analysis should be ignored (no analysis discarded).
                # In principle, there is also one tag for which it should be done if the word is in the first position:
                # NP00000 @begin
                # This is not yet implemented and will lead to mismatches with the old treebanks, especially with proper names.
                if w.get_form().lower() in override_dicts['no_disambiguate']:
                    additional_arcs.append(({'additional': True, 'tag': a.get_tag(), 'prob': a.get_prob(), 'lemma': a.get_lemma()}))
                    #print("Non-selected analysis: {}".format(a.get_tag()))
        return tags, additional_arcs
