(in-package :tsdb)

(setf *feature-grandparenting* 2)

(setf *feature-use-preterminal-types-p* t)

(setf *feature-lexicalization-p* nil)

(setf *feature-constituent-weight* 0)

(setf *feature-active-edges-p* nil)

(setf *feature-ngram-size* 0)

(setf *feature-ngram-tag* :type)

(setf *feature-ngram-back-off-p* t)

(setf *feature-item-enhancers* nil)

(setf *feature-lm-p* nil)

(setf *feature-preference-weightings* '((0 :binary)))

(setf *feature-random-sample-size* nil)

(setf %redwoods-items-increment% #-:64bit 100 #+:64bit 200)

(setf %redwoods-items-percentile% 20)
