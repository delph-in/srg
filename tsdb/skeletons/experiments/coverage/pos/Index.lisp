
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

(((:path . "an05") (:content . "Tibidabo (5 Word)"))
 ((:path . "an10") (:content . "Tibidabo (10 Words)"))
 ((:path . "an15") (:content . "Tibidabo (15 Words)"))
 ((:path . "an20") (:content . "Tibidabo (20 Words)"))
 ((:path . "an25") (:content . "Tibidabo (25 Words)"))
 ((:path . "an30") (:content . "Tibidabo (30 Words)"))
 ((:path . "an35") (:content . "Tibidabo (35 Words)"))
 ((:path . "an40") (:content . "Tibidabo (40 Words)"))
 ((:path . "an45") (:content . "Tibidabo (45 Words)"))
 ((:path . "an50") (:content . "Tibidabo (50 Words)"))
 ((:path . "an55") (:content . "Tibidabo (55 Words)"))
 ((:path . "an60") (:content . "Tibidabo (60 Words)"))
 ((:path . "an65") (:content . "Tibidabo (65 Words)"))
 ((:path . "an70") (:content . "Tibidabo (70 Words)"))
 ((:path . "an75") (:content . "Tibidabo (75 Words)"))
 ((:path . "an80") (:content . "Tibidabo (80 Words)"))
 ((:path . "an85") (:content . "Tibidabo (85 Words)"))
 ((:path . "an90") (:content . "Tibidabo (90 Words)"))
 ((:path . "an95") (:content . "Tibidabo (95 Words)"))
 ((:path . "an100") (:content . "Tibidabo (100 Words)")))

