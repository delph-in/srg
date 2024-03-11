;;; patches.lsp file to make YY input mode work properly with generic lexical entries
;;; Only use with LKB-FOS version of 20-Jun-2023
;;;
;;; Version 2 of 5-Mar-2024

(in-package :tsdb)

(defun yy-read-input (string &key (format :string) (sort :id))
  ;; (id, start, end, [link,] path+, form [surface], ipos, lrule+ [,{pos prob}+])
  (let* ((i 0)
         (length (length string))
         (whitespace '(#\space #\tab #\newline)))
    (labels ((skip (characters)
               (loop
                   while (member (schar string i) characters :test #'char=)
                   do (incf i)))
             (skip-to (character)
               (loop
                   with escape = nil with quote = nil
                   while (< i length)
                   when (and (char= (schar string i) #\") (not escape))
                   do (setf quote (not quote))
                   else when (and (char= (schar string i) #\\) (not escape))
                   do (setf escape t)
                   else when (and (char= (schar string i) character) 
                                  (not quote))
                   return i
                   else do (setf escape nil)
                   do (incf i)))
             (seek-character (character)
               (when (< i length)
                 (skip whitespace)
                 (char= (schar string i) character)))
             (read-character (character)
               (when (seek-character character)
                 (incf i)))
             (read-integer ()
               (when (< i length)
                 (multiple-value-bind (int rest)
                     (parse-integer string :start i :junk-allowed t)
                   (when int
                     (setf i rest)
                     int))))
             (read-characterization ()
               (when (seek-character #\<)
                 (let ((*readtable* (copy-readtable))
                       from to)
                   (set-syntax-from-char #\: #\" *readtable*)
                   (set-syntax-from-char #\, #\" *readtable*)
                   (set-syntax-from-char #\> #\" *readtable*)
                   (read-character #\<)
                   (setf from (read-integer))
                   (when (numberp from)
                     (read-character #\:)
                     (setf to (read-integer))
                     (read-character #\>)
                     (read-character #\,)
                     (and (numberp to) (values from to))))))
             (read-string ()
               (seek-character #\")
               (when (< i length)
                 (let* ((r1 (search "\" " string :start2 (1+ i)))
                        (r2 (search "\", " string :start2 (1+ i)))
                        (rest (or (and (and r1 r2) (min r1 r2)) r1 r2)))
                   (when rest
                     (prog1
                       (cl-ppcre:regex-replace-all ; fix up extra escaping of double quote
                         '(:sequence #\\ #\")
                         (subseq string (1+ i) rest)
                         '("\""))
                       (setf i (1+ rest)))))))
             (read-number ()
               (skip whitespace)
               (when (< i length)
                 (let ((rest (loop for n from i
                                 while (< i length)
                                 unless (or (digit-char-p (schar string n))
                                            (member (schar string n) '(#\. #\-)))
                                 return n)))
                   (when rest
                     (prog1
                       (read-from-string string nil nil :start i :end rest)
                       (setf i rest))))))
             (read-token ()
               (progn ; JAC 19-Jun-2023: was ignore-errors, which masked some incorrect behaviour
                (let (id start end from to form surface inflection tags)
                  (when (read-character #\()
                    (setf id (read-integer))
                    (read-character #\,)
                    (setf start (read-integer))
                    (read-character #\,)
                    (setf end (read-integer))
                    (read-character #\,)
                    (multiple-value-setq (from to) (read-characterization))
                    ;;
                    ;; skip over the path(s) this token is a member of; we are
                    ;; assuming everything is connected with everything.
                    ;;
                    (skip-to #\,) (read-character #\,)
                    (setf form (read-string))
                    (when (seek-character #\") (setf surface (read-string)))
                    (read-character #\,)
                    ;;
                    ;; skip over the inflection position (ipos) field
                    ;;
                    (skip-to #\,) (read-character #\,)
                    ;;
                    ;; inflection is a list of elements (was originally a singleton)
                    ;;
                    (setf inflection (list (read-string)))
                    (loop 
                      (if (seek-character #\")
                          (setf inflection (append inflection (list (read-string))))
                          (return)))
                    ;;
                    ;; PoS and probability field; missing probs default to 0.0
                    ;;
                    (when (seek-character #\,)
                      (read-character #\,)
                      (setf tags
                        (loop
                            while (and (< i length) (not (seek-character #\))))
                            nconc (list (read-string) (or (read-number) 0.0)))))
                    (skip-to #\))
                    (when (read-character #\))
                      (pairlis '(:id :start :end :from :to 
                                 :form :surface :inflection :tags)
                               (list id start end from to
                                     form surface inflection tags))))))))
      (let ((tokens (loop for token = (read-token) while token collect token)))
        (setf tokens
          (case sort
            (:id
             (sort tokens #'< :key #'(lambda (token) (get-field :id token))))
            (t
             (sort
              tokens
              #'(lambda (token1 token2)
                  (let ((start1 (get-field :start token1))
                        (end1 (get-field :end token1))
                        (start2 (get-field :start token2))
                        (end2 (get-field :end token2)))
                    (when (and (numberp start1) (numberp end1)
                               (numberp start2) (numberp end2))
                      (or (< start1 start2)
                          (and (= start1 start2) (< end1 end2))
                          (and (= start1 start2) (= end1 end2)
                               (string< (get-field :form token1)
                                        (get-field :form token2)))))))))))
        (case format
          (:raw
           tokens)
          (:string
           (loop
               with result =
                 (make-array length
                  :element-type 'character :adjustable nil :fill-pointer 0)
               with positions = nil
               with ntokens = 0
               for token in tokens
               for start = (get-field :start token)
               for word = (get-field :form token)
               unless (member start positions :test #'=)
               do 
                  (push start positions)
                  (unless (zerop ntokens) (vector-push #\space result))
                  (loop for c across word do (vector-push c result))
                  (incf ntokens)
               finally (return (unless (equal result "") result)))))))))

(in-package :lkb)

(defmacro token-edge-partial-tree (e) ; _fix_me_ just for now repurpose unused maf-id field
  `(token-edge-maf-id ,e))

(defun yy-setup-morphs (tokens)
  ;; each token is e.g.
  ;; ((:TAGS "vmm03p0" 0.0 "+pp3cn00" 1.0) (:INFLECTION "vmm03p0" "+pp3cn00")
  ;;  (:SURFACE . "imagínense") (:FORM . "imaginar") (:TO . 10) (:FROM . 0)
  ;;  (:END . 1) (:START . 0) (:ID . 1))
  (loop
      for token in tokens
      for surface = (rest (assoc :surface token))
      for start = (or (rest (assoc :start token)) -1)
      for end = (or (rest (assoc :end token)) -1)
      for from = (or (rest (assoc :from token)) -1)
      for to = (or (rest (assoc :to token)) -1)
      for stem = (string-upcase (rest (assoc :form token)))
      for rule = (rest (assoc :inflection token))
      for partial-tree
        = (if (member rule '("null" ("null")) :test #'equal)
              nil ; activate built-in morphology mode
              (loop for r in (if (consp rule) rule (list rule)) ; was originally a singleton
                collect (list (intern (string-upcase r) :lkb) surface)))
      for edge
        = (add-token-edge surface (string-upcase surface) start end from to)
      do
        (when *token-type*
          ;; although we don't allow token mapping rules to be applied to YY format
          ;; input, we do support activation of generic lexical entries via token FS
          (create-token-edge-dag edge (rest (assoc :id token)) (rest (assoc :tags token)))
          ;; make partial-tree info available when adding generic lexical entry edges
          (setf (token-edge-partial-tree edge) partial-tree))
        (add-morpho-stem-edge
          stem partial-tree
          start end (string-upcase surface) surface from to
          (token-edge-leaves edge) edge)))

(defun add-token-edge (base-word word from to cfrom cto)
  ;; e.g. (add-token-edge "The" "THE" 0 1 nil nil)
  (when (> to *tchart-max*)
    (setf *tchart-max* to))
  (let (; (existing-edges (aref *tchart* to 0)) ; JAC 29-Nov-2023 - see below
	(edge (make-token-edge :id (next-edge)
			       :string base-word
			       :word word
			       :leaves (list base-word)
			       :from from
			       :to to
			       :cfrom cfrom
			       :cto cto)))
    (unless nil ; JAC 29-Nov-2023 - removed sloppy (token-edge-match edge existing-edges)
      (push edge (aref *tchart* to 0))
      (push edge (aref *tchart* from 1))
      edge)))

(defun add-generic-lexical-entries (tedge)
  (let* ((word (token-edge-word tedge))
         (string (token-edge-string tedge))
         (from (token-edge-from tedge))
         (to (token-edge-to tedge))
         (cfrom (token-edge-cfrom tedge))
         (cto (token-edge-cto tedge))
         (pt (token-edge-partial-tree tedge)) ; only applicable for YY mode
         (stem-and-pt-list
           (if pt ; e.g. from YY format preprocessor analysis
               (list (cons word pt))
               (let ((*lexicon* 'identity)) (get-morph-analyses word))))
         (glex (lex "gle")))
    ;; Most grammars that perform token mapping also define a generic lexical entry file.
    ;; Therefore check that the file has been loaded correctly (i.e. as a _sub-lexicon_)
    ;; since this is easy to get wrong. The grammarian should supply an empty file if
    ;; there really are no generic lexical entries.
    (unless glex
      (error "Could not find sub-lexicon \"gle\" when looking for generic lexical entries"))
    (loop for gid in (collect-psort-ids glex)
        for entry = (get-lex-entry-from-id gid)
        do
        (loop for (stem . partial-tree) in stem-and-pt-list
            do
            (let ((*lexical-entries-used* nil))
              (add-stem-edge stem string
                             from to cfrom cto
                             partial-tree
                             entry (list tedge)))))))

(defun add-stem-edge (edge-stem edge-string
                      from to cfrom cto partial-tree entry dtrs)
  #+:arboretum (declare (special *mal-active-p*))
  (let ((expanded-entry (get-expanded-lex-entry entry)))
    (when (and expanded-entry
               #+:arboretum
               (or *mal-active-p* 
                   (not (mal-lex-entry-p expanded-entry))))
      (let* ((fs
               (copy-lex-fs-as-needed (lex-entry-full-fs entry)))
             (new-fs
               (cond
                 ((edge-dag (car dtrs))
                   (unify-in-tokens-list fs (mapcar #'edge-dag dtrs)))
                 (*characterize-p*
                   (set-characterization-tdfs fs cfrom cto))
                 (t fs))))
        (when new-fs
          (let
            ((new-edge
               (make-edge :id (next-edge) 
                          :category (indef-type-of-tdfs new-fs)
                          :rule edge-stem
                          :dag new-fs
                          :dag-restricted (restrict-fs (tdfs-indef new-fs))
                          :leaves (list edge-string)
                          :lex-ids (list (lex-entry-id entry))
                          :from from :to to
                          :tchildren dtrs
                          :partial-tree partial-tree
                          :string edge-string
                          :cfrom cfrom :cto cto)))
            (when *cm-debug*
              (format t
"~&Adding edge ~D for lexical entry ~(~A~) `~A'~@[ requiring ~{~(~A~)~^, ~}~]~%"
                (edge-id new-edge) (lex-entry-id entry) edge-string
                (mapcar #'car partial-tree)))
            (push new-edge (aref *chart* from to))))))))
