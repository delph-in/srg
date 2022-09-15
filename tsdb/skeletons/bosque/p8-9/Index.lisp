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

(((:path . "dtv0p8-9_bea_168") (:content . "Bosque (8 to 9 words, 0 verb, serie 168 )"))
 ((:path . "dtv0p8-9_bea_169") (:content . "Bosque (8 to 9 words, 0 verb, serie 169 )"))
 ((:path . "dtv1p8-9_bea_170") (:content . "Bosque (8 to 9 words, 1 verb, serie 170 )"))
 ((:path . "dtv1p8-9_bea_171") (:content . "Bosque (8 to 9 words, 1 verb, serie 171 )"))
 ((:path . "dtv0p8-9_bea_199") (:content . "Bosque (8 to 9 words, 0 verb, serie 199 )"))
 ((:path . "dtv0p8-9_bea_200") (:content . "Bosque (8 to 9 words, 0 verb, serie 200 )"))
 ((:path . "dtv1p8-9_bea_201") (:content . "Bosque (8 to 9 words, 1 verb, serie 201 )"))
 ((:path . "dtv1p8-9_bea_202") (:content . "Bosque (8 to 9 words, 1 verb, serie 202)")))
