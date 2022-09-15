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

(((:path . "DtV0P10-11_Bea_172") (:content . "Bosque (10 to 11 words, 0 verb, serie 172 )"))
 ((:path . "dtv0p10-11_bea_203") (:content . "Bosque (10 to 11 words, 0 verb, serie 203 )"))
 ((:path . "DtV1P10-11_Bea_173") (:content . "Bosque (10 to 11 words, 1 verb, serie 173 )"))
 ((:path . "DtV1P10-11_Bea_174") (:content . "Bosque (10 to 11 words, 1 verb, serie 174 )"))
 ((:path . "dtv1p10-11_bea_204") (:content . "Bosque (10 to 11 words, 0 verb, serie 204 )"))
 ((:path . "dtv1p10-11_bea_205") (:content . "Bosque (10 to 11 words, 0 verb, serie 205 )")))
