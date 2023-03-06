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
;;;  ((:path . "p12-13") (:content . "Bosque (12-13 words)")))

;;; ((:path . "DtV1P4-7_Bea_002") (:content . "Bosque (DtV1P4-7_Bea_002)"))
;;; ((:path . "DtV1P4-7_Bea_003") (:content . "Bosque (DtV1P4-7_Bea_003)"))
;;; ((:path . "DtV1P4-7_Bea_004") (:content . "Bosque (DtV1P4-7_Bea_004)"))
;;; ((:path . "DtV1P4-7_Bea_005") (:content . "Bosque (DtV1P4-7_Bea_005)"))
;;; ((:path . "DtV1P4-7_Bea_006") (:content . "Bosque (DtV1P4-7_Bea_006)"))
;;; ((:path . "DtV1P4-7_Bea_007") (:content . "Bosque (DtV1P4-7_Bea_007)"))
;;; ((:path . "DtV1P4-7_Bea_008") (:content . "Bosque (DtV1P4-7_Bea_008)"))
;;; ((:path . "DtV1P4-7_Bea_009") (:content . "Bosque (DtV1P4-7_Bea_009)"))
;;; ((:path . "DtV1P4-7_Bea_010") (:content . "Bosque (DtV1P4-7_Bea_010)"))
;;; ((:path . "DtV1P4-7_Bea_011") (:content . "Bosque (DtV1P4-7_Bea_011)"))
;;; ((:path . "DtV1P4-7_Bea_012") (:content . "Bosque (DtV1P4-7_Bea_012)"))
;;; ((:path . "DtV1P4-7_Bea_013") (:content . "Bosque (DtV1P4-7_Bea_013)"))
;;; ((:path . "DtV1P4-7_Bea_014") (:content . "Bosque (DtV1P4-7_Bea_014)"))
;;; ((:path . "DtV1P4-7_Bea_015") (:content . "Bosque (DtV1P4-7_Bea_015)"))
;;; ((:path . "DtV1P4-7_Bea_016") (:content . "Bosque (DtV1P4-7_Bea_016)"))
;;; ((:path . "DtV1P4-7_Bea_017") (:content . "Bosque (DtV1P4-7_Bea_017)"))
;;; ((:path . "DtV1P4-7_Bea_018") (:content . "Bosque (DtV1P4-7_Bea_018)"))
;;; ((:path . "DtV0P4-7_Bea_143") (:content . "Bosque (DtV0P4-7_Bea_143)"))
;;; ((:path . "DtV0P4-7_Bea_144") (:content . "Bosque (DtV0P4-7_Bea_144)"))
;;; ((:path . "DtV0P4-7_Bea_150") (:content . "Bosque (DtV0P4-7_Bea_150)"))
;;; ((:path . "DtV0P4-7_Bea_152") (:content . "Bosque (DtV0P4-7_Bea_152)"))
;;; ((:path . "DtV0P4-7_Bea_151") (:content . "Bosque (DtV0P4-7_Bea_151)"))
;;; ((:path . "DtV0P4-7_Bea_154") (:content . "Bosque (DtV0P4-7_Bea_154)"))
;;; ((:path . "DtV0P4-7_Bea_155") (:content . "Bosque (DtV0P4-7_Bea_155)"))
;;; ((:path . "DtV0P4-7_Bea_156") (:content . "Bosque (DtV0P4-7_Bea_156)"))
;;; ((:path . "DtV0P4-7_Bea_157") (:content . "Bosque (DtV0P4-7_Bea_157)"))
;;; ((:path . "DtV0P4-7_Bea_158") (:content . "Bosque (DtV0P4-7_Bea_158)"))
;;; ((:path . "DtV0P4-7_Bea_159") (:content . "Bosque (DtV0P4-7_Bea_159)"))
;;; ((:path . "DtV0P4-7_Bea_160") (:content . "Bosque (DtV0P4-7_Bea_160)"))
;;; ((:path . "DtV0P4-7_Bea_161") (:content . "Bosque (DtV0P4-7_Bea_161)"))
;;; ((:path . "DtV0P8-9_Bea_168") (:content . "Bosque (DtV0P8-9_Bea_168)"))
;;; ((:path . "DtV0P8-9_Bea_169") (:content . "Bosque (DtV0P8-9_Bea_169)"))
;;; ((:path . "DtV1P8-9_Bea_170") (:content . "Bosque (DtV1P8-9_Bea_170)"))
;;; ((:path . "DtV1P8-9_Bea_171") (:content . "Bosque (DtV1P8-9_Bea_171)"))
;;; ((:path . "DtV0P10-11_Bea_172") (:content . "Bosque (DtV0P10-11_Bea_172)"))
;;; ((:path . "DtV1P10-11_Bea_173") (:content . "Bosque (DtV1P10-11_Bea_173)"))
;;; ((:path . "DtV1P10-11_Bea_174") (:content . "Bosque (DtV1P10-11_Bea_174)"))

(((:path . "DtV1P12-13_Bea_175") (:content . "Bosque (DtV1P12-13_Bea_175)"))
 ((:path . "DtV0P12-13_Bea_176") (:content . "Bosque (DtV0P12-13_Bea_176)"))
 ((:path . "DtV1P12-13_Bea_177") (:content . "Bosque (DtV1P12-13_Bea_177)"))
 ((:path . "DtV1P12-13_Bea_178") (:content . "Bosque (DtV1P12-13_Bea_178)"))
 ((:path . "DtV1P12-13_Bea_179") (:content . "Bosque (DtV1P12-13_Bea_179)"))
 ((:path . "DtV2P12-13_Bea_180") (:content . "Bosque (DtV2P12-13_Bea_180)")))