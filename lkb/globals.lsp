;;; LinGO grammar specific globals file
;;; parameters only - grammar specific functions 
;;; should go in user-fns.lsp


(defparameter *active-parsing-p* t)

;;; Strings

(defparameter *toptype* '*top*)

(defparameter *string-type* 'string
   "a special type name - any lisp strings are subtypes of it")

;;; Lexical files

(defparameter *orth-path* '(stem))

(defparameter *list-tail* '(rest))

(defparameter *list-head* '(first))

(defparameter *empty-list-type* 'null)

(defparameter *list-type* 'list)

(defparameter *diff-list-type* 'diff-list)

(defparameter *diff-list-list* 'list)

(defparameter *diff-list-last* 'last)

;(defparameter *lex-rule-suffix* "_INFL_RULE"
; "creates the inflectional rule name from the information
;  in irregs.tab - for PAGE compatability")

(defparameter *irregular-forms-only-p* t)

;;;
;;; tokenization is done externally, so *punctuation-characters* setting is irrelevant
;;;
;(defparameter *punctuation-characters*
;  '(#\space #\[ #\] #\{ #\} #\> #\< #\* #\+ #\= #\/ #\-))

(defparameter *display-type-hierarchy-on-load* nil)

;;; Parsing

(defparameter *chart-limit* 100
  "maximum number of tokens in a sentence to be parsed")

(defparameter *maximum-number-of-edges* 10000
  "limits the size of the parsing/generation chart")

(defparameter *mother-feature* nil
  "the feature giving the mother in a grammar rule")

(defparameter *start-symbol* '(root_vp_inf root_s root_vpnom root_np root_nbar root_pp root_ap root_rp root_c root_i)
  "specifing valid parses")

(defparameter *maximal-lex-rule-applications* 20
  "the number of lexical rule applications which may be made
   before it is assumed that some rules are applying circularly")

(defparameter *deleted-daughter-features* 
  '(ARGS HEAD-DTR NON-HEAD-DTR LCOORD-DTR RCOORD-DTR CONJ-DTR NONCONJ-DTR) 
  "features pointing to daughters deleted on building a constituent")

;;;
;;; enable local ambiguity packing
;;;
(defparameter *chart-packing-p* t)

(defparameter *packing-restrictor*
  '(RELS HCONS ICONS RNAME)
  "restrictor used when parsing with ambiguity packing")

;;; Parse tree node labels

;;; the path where the name string is stored
(defparameter *label-path* '(LABEL-NAME))

;;; the path for the meta prefix symbol
(defparameter *prefix-path* '(META-PREFIX))

;;; the path for the meta suffix symbol
(defparameter *suffix-path* '(META-SUFFIX))

;;; the path for the recursive category
(defparameter *recursive-path* '(SYNSEM NON-LOCAL SLASH LIST FIRST))

;;; the path inside the node to be unified with the recursive node
(defparameter *local-path* '(SYNSEM LOCAL))

;;; the path inside the node to be unified with the label node
(defparameter *label-fs-path* '())

(defparameter *label-template-type* 'label)

;;; for the compare function 

(defparameter *discriminant-path* '(synsem local keys key pred))

;;; the lex-rule suffix defaults to _lex_rule, but this might
;;; not be desirable

(setf *lex-rule-suffix* nil)

(setf cdb::*cdb-ascii-p* nil)

;;;
;;; chart mapping is enabled by setting *token-type* to the name of the token
;;; type (standardly, `token'). Token feature structures have type *token-type*
;;; and consist of grammar-specific bundles of properties that were input to
;;; parsing; to access individual components, there are a number of
;;; (customizable) paths.
;;;
(def-lkb-parameter *token-type* 'token)

(def-lkb-parameter *token-form-path* '(+FORM))
(def-lkb-parameter *token-id-path* '(+ID))
(def-lkb-parameter *token-from-path* '(+FROM))
(def-lkb-parameter *token-to-path* '(+TO))
(def-lkb-parameter *token-postags-path* '(+POS +TAGS))
(def-lkb-parameter *token-posprobs-path* '(+POS +PRBS))

;;;
;;; when token mapping is enabled, lexical entries behave similarly to grammar
;;; rules in one respect: the list of input tokens that license a lexical entry
;;; are unified into *lexicon-tokens-path*.  furthermore, to give the
;;; grammarian easier access to the token in the right periphery, the last element
;;; of the tokens list is made re-entrant with *lexicon-last-token-path*.
;;;
(def-lkb-parameter *lexicon-tokens-path* '(TOKENS +LIST))
(def-lkb-parameter *lexicon-last-token-path* '(TOKENS +LAST))

;;;
;;; chart mapping rules consist of between 1 and 5 components (the minimum being
;;; a single input FS)
;;;
(def-lkb-parameter *chart-mapping-context-path* '(+CONTEXT))
(def-lkb-parameter *chart-mapping-input-path* '(+INPUT))
(def-lkb-parameter *chart-mapping-output-path* '(+OUTPUT))
(def-lkb-parameter *chart-mapping-position-path* '(+POSITION))
(def-lkb-parameter *chart-mapping-jump-path* '(+JUMP))

;;;
;;; Preprocessing is performed by FreeLing, and its output is converted to the
;;; DELPH-IN YY format for parsing.
;;;
(defparameter *fl-application* "bash ~/delphin/srg/util/srg-yy-python-api.sh")
