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


;;; (((:path . "p4-7") (:content . "Bosque (4-7 words)"))
;;;  ((:path . "p8-9") (:content . "Bosque (8-9 words)"))
;;;  ((:path . "p10-11") (:content . "Bosque (10-11 words)"))
;;;  ((:path . "p12-13") (:content . "Bosque (12-13 words)"))
;;;  ((:path . "p14-15") (:content . "Bosque (14-15 words)")))


(((:path . "DtV0P14-15_Bea_182") (:content . "Bosque (DtV0P14-15_Bea_182)"))
 ((:path . "DtV1P14-15_Bea_183") (:content . "Bosque (DtV1P14-15_Bea_183)"))
 ((:path . "DtV1P14-15_Bea_184") (:content . "Bosque (DtV1P14-15_Bea_184)"))
 ((:path . "DtV1P14-15_Bea_185") (:content . "Bosque (DtV1P14-15_Bea_185)"))
 ((:path . "DtV2P14-15_Bea_186") (:content . "Bosque (DtV2P14-15_Bea_186)")))