(in-package :lkb)

#-:logon
(defun sppp-serialize-tokens (tokens)
  #+:debug
  (setf %tokens tokens)
  (let* ((n (loop
                for token in tokens
                maximize (rest (assoc :to token))))
         (map (make-array (+ n 1))))
    (loop
        for i from 0 to n
        do (setf (aref map i) (cons nil nil)))
    (loop
        for token in tokens
        for from = (rest (assoc :from token))
        for to = (rest (assoc :to token))
        do
          (setf (first (aref map from)) t)
          (setf (rest (aref map to)) t))
    (loop
        with last = 0 with endp = t
        for i from 0 to n
        when (first (aref map i)) do
          (unless endp (incf last))
          (setf (first (aref map i)) last)
          (setf endp nil)
        when (rest (aref map i)) do
          (unless (eql (first (aref map i)) last) (incf last))
          (setf (rest (aref map i)) last)
          (setf endp t))
    (loop
        for token in tokens
        for from = (rest (assoc :from token))
        for to = (rest (assoc :to token))
        for start = (first (aref map from))
        for end = (rest (aref map to))
        do (nconc token (pairlis '(:start :end) (list start end))))
    tokens))

;;;
;;; the LOGON tree has a few defaults set differently from the plain DELPH-IN
;;; versions of the LKB, [incr tsdb()], et al.  adjust values as needed for use
;;; with the SRG.                                               (17-sep-07; oe)
;;; 
#+:logon
(progn
 (setf lkb::*tree-discriminants-mode* :classic)
 (setf tsdb::*process-raw-print-trace-p* t))
