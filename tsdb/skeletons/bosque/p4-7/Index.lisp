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

(((:path . "dtv0p4-7_bea_143") (:content . "Bosque (4 to 7 words, 0 verb, serie 143 )"))
 ((:path . "dtv0p4-7_bea_144") (:content . "Bosque (4 to 7 words, 0 verb, serie 144 )"))
 ((:path . "dtv0p4-7_bea_150") (:content . "Bosque (4 to 7 words, 0 verb, serie 150 )"))
 ((:path . "dtv0p4-7_bea_151") (:content . "Bosque (4 to 7 words, 0 verb, serie 151 )"))
 ((:path . "dtv0p4-7_bea_152") (:content . "Bosque (4 to 7 words, 0 verb, serie 152 )"))
 ((:path . "dtv0p4-7_bea_154") (:content . "Bosque (4 to 7 words, 0 verb, serie 154 )"))
 ((:path . "dtv0p4-7_bea_155") (:content . "Bosque (4 to 7 words, 0 verb, serie 155 )"))
 ((:path . "dtv0p4-7_bea_156") (:content . "Bosque (4 to 7 words, 0 verb, serie 156 )"))
 ((:path . "dtv0p4-7_bea_157") (:content . "Bosque (4 to 7 words, 0 verb, serie 157 )"))
 ((:path . "dtv0p4-7_bea_158") (:content . "Bosque (4 to 7 words, 0 verb, serie 158 )"))
 ((:path . "dtv0p4-7_bea_159") (:content . "Bosque (4 to 7 words, 0 verb, serie 159 )"))
 ((:path . "dtv0p4-7_bea_160") (:content . "Bosque (4 to 7 words, 0 verb, serie 160 )"))
 ((:path . "dtv0p4-7_bea_161") (:content . "Bosque (4 to 7 words, 0 verb, serie 161 )"))
 ((:path . "dtv1p4-7_bea_001") (:content . "Bosque (4 to 7 words, 1 verb, serie 1 )"))
 ((:path . "dtv1p4-7_bea_002") (:content . "Bosque (4 to 7 words, 1 verb, serie 2 )"))
 ((:path . "dtv1p4-7_bea_003") (:content . "Bosque (4 to 7 words, 1 verb, serie 3 )"))
 ((:path . "dtv1p4-7_bea_004") (:content . "Bosque (4 to 7 words, 1 verb, serie 4 )"))
 ((:path . "dtv1p4-7_bea_005") (:content . "Bosque (4 to 7 words, 1 verb, serie 5 )"))
 ((:path . "dtv1p4-7_bea_006") (:content . "Bosque (4 to 7 words, 1 verb, serie 6 )"))
 ((:path . "dtv1p4-7_bea_007") (:content . "Bosque (4 to 7 words, 1 verb, serie 7 )"))
 ((:path . "dtv1p4-7_bea_008") (:content . "Bosque (4 to 7 words, 1 verb, serie 8 )"))
 ((:path . "dtv1p4-7_bea_009") (:content . "Bosque (4 to 7 words, 1 verb, serie 9 )"))
 ((:path . "dtv1p4-7_bea_010") (:content . "Bosque (4 to 7 words, 1 verb, serie 10 )"))
 ((:path . "dtv1p4-7_bea_011") (:content . "Bosque (4 to 7 words, 1 verb, serie 11 )"))
 ((:path . "dtv1p4-7_bea_012") (:content . "Bosque (4 to 7 words, 1 verb, serie 12 )"))
 ((:path . "dtv1p4-7_bea_013") (:content . "Bosque (4 to 7 words, 1 verb, serie 13 )"))
 ((:path . "dtv1p4-7_bea_014") (:content . "Bosque (4 to 7 words, 1 verb, serie 14 )"))
 ((:path . "dtv1p4-7_bea_015") (:content . "Bosque (4 to 7 words, 1 verb, serie 15 )"))
 ((:path . "dtv1p4-7_bea_016") (:content . "Bosque (4 to 7 words, 1 verb, serie 16 )"))
 ((:path . "dtv1p4-7_bea_017") (:content . "Bosque (4 to 7 words, 1 verb, serie 17 )"))
 ((:path . "dtv1p4-7_bea_018") (:content . "Bosque (4 to 7 words, 1 verb, serie 18 )")))
