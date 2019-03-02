;; Auto-generated. Do not edit!


(when (boundp 'task1::Test)
  (if (not (find-package "TASK1"))
    (make-package "TASK1"))
  (shadow 'Test (find-package "TASK1")))
(unless (find-package "TASK1::TEST")
  (make-package "TASK1::TEST"))

(in-package "ROS")
;;//! \htmlinclude Test.msg.html


(defclass task1::Test
  :super ros::object
  :slots (_content _number ))

(defmethod task1::Test
  (:init
   (&key
    ((:content __content) "")
    ((:number __number) 0)
    )
   (send-super :init)
   (setq _content (string __content))
   (setq _number (round __number))
   self)
  (:content
   (&optional __content)
   (if __content (setq _content __content)) _content)
  (:number
   (&optional __number)
   (if __number (setq _number __number)) _number)
  (:serialization-length
   ()
   (+
    ;; string _content
    4 (length _content)
    ;; int16 _number
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _content
       (write-long (length _content) s) (princ _content s)
     ;; int16 _number
       (write-word _number s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _content
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _content (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int16 _number
     (setq _number (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get task1::Test :md5sum-) "457e7dfc51876192fa55da49de0e384a")
(setf (get task1::Test :datatype-) "task1/Test")
(setf (get task1::Test :definition-)
      "string content
int16 number

")



(provide :task1/Test "457e7dfc51876192fa55da49de0e384a")


