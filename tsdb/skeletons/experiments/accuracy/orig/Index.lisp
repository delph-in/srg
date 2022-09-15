
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

(((:path . "an01") (:content . "(1 Word)"))
 ((:path . "an02") (:content . "(2 Words)"))
 ((:path . "an03") (:content . "(3 Words)"))
 ((:path . "an04") (:content . "(4 Words)"))
 ((:path . "an05") (:content . "(5 Words)"))
 ((:path . "an06") (:content . "(6 Words)"))
 ((:path . "an07") (:content . "(7 Words)"))
 ((:path . "an08") (:content . "(8 Words)"))
 ((:path . "an09") (:content . "(9 Words)"))
 ((:path . "an10") (:content . "(10 Words)"))
 ((:path . "an11") (:content . "(11 Words)"))
 ((:path . "an12") (:content . "(12 Words)"))
 ((:path . "an13") (:content . "(13 Words)"))
 ((:path . "an14") (:content . "(14 Words)"))
 ((:path . "an15") (:content . "(15 Words)"))
 ((:path . "an16") (:content . "(16 Words)"))
 ((:path . "an17") (:content . "(17 Words)"))
 ((:path . "an18") (:content . "(18 Words)"))
 ((:path . "an19") (:content . "(19 Words)"))
 ((:path . "an20") (:content . "(20 Words)")))
