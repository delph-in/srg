
;;;
;;; this file should be `Index.lisp' and reside in the directory containing the
;;; tsdb(1) test suite skeleton databases (typically a subdirectory `skeletons'
;;; in the tsdb(1) database root directory `*tsdb-home*').
;;;
;;; the file should contain a single un-quote()d Common-Lisp list enumerating
;;; the available skeletons, e.g.
;;;
;;;   (((:path . "english") (:content . "English TSNLP test suite"))
;;;    ((:path . "csli") (:content . "CSLI (ERGO) test suite"))
;;;    ((:path . "vm") (:content . "English VerbMobil data")))
;;;
;;; where the individual entries are assoc() lists with at least two elements:
;;;
;;;   - :path --- the (relative) directory name containing the skeleton;
;;;   - :content --- a descriptive comment.
;;;
;;; the order of entries is irrelevant as the `tsdb :skeletons' command sorts
;;; the list lexicographically before output.
;;;

(((:path . "ts0") (:content . "(1 Word)"))
 ((:path . "ts1") (:content . "(2 Words)"))
 ((:path . "ts2") (:content . "(3 Words)"))
 ((:path . "ts3") (:content . "(4 Words)"))
 ((:path . "ts4") (:content . "(5 Words)"))
 ((:path . "tr0") (:content . "(6 Words)"))
 ((:path . "tr1") (:content . "(7 Words)"))
 ((:path . "tr2") (:content . "(8 Words)"))
 ((:path . "tr3") (:content . "(9 Words)"))
 ((:path . "tr4") (:content . "(10 Words)")))
