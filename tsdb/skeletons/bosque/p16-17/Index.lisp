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


(((:path . "DtV0P16-17_Bea_187") (:content . "Bosque (DtV0P16-17_Bea_187)"))
 ((:path . "DtV1P16-17_Bea_188") (:content . "Bosque (DtV1P16-17_Bea_188)"))
 ((:path . "DtV1P16-17_Bea_189") (:content . "Bosque (DtV1P16-17_Bea_189)"))
 ((:path . "DtV1P16-17_Bea_190") (:content . "Bosque (DtV1P16-17_Bea_190)"))
 ((:path . "DtV2P16-17_Bea_191") (:content . "Bosque (DtV2P16-17_Bea_191)")))