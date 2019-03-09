;; Auto-generated. Do not edit!


(when (boundp 'exercise2::move)
  (if (not (find-package "EXERCISE2"))
    (make-package "EXERCISE2"))
  (shadow 'move (find-package "EXERCISE2")))
(unless (find-package "EXERCISE2::MOVE")
  (make-package "EXERCISE2::MOVE"))
(unless (find-package "EXERCISE2::MOVEREQUEST")
  (make-package "EXERCISE2::MOVEREQUEST"))
(unless (find-package "EXERCISE2::MOVERESPONSE")
  (make-package "EXERCISE2::MOVERESPONSE"))

(in-package "ROS")





(defclass exercise2::moveRequest
  :super ros::object
  :slots (_shape _time ))

(defmethod exercise2::moveRequest
  (:init
   (&key
    ((:shape __shape) "")
    ((:time __time) 0)
    )
   (send-super :init)
   (setq _shape (string __shape))
   (setq _time (round __time))
   self)
  (:shape
   (&optional __shape)
   (if __shape (setq _shape __shape)) _shape)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:serialization-length
   ()
   (+
    ;; string _shape
    4 (length _shape)
    ;; int32 _time
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _shape
       (write-long (length _shape) s) (princ _shape s)
     ;; int32 _time
       (write-long _time s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _shape
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _shape (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int32 _time
     (setq _time (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass exercise2::moveResponse
  :super ros::object
  :slots (_lastShape ))

(defmethod exercise2::moveResponse
  (:init
   (&key
    ((:lastShape __lastShape) "")
    )
   (send-super :init)
   (setq _lastShape (string __lastShape))
   self)
  (:lastShape
   (&optional __lastShape)
   (if __lastShape (setq _lastShape __lastShape)) _lastShape)
  (:serialization-length
   ()
   (+
    ;; string _lastShape
    4 (length _lastShape)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _lastShape
       (write-long (length _lastShape) s) (princ _lastShape s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _lastShape
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _lastShape (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass exercise2::move
  :super ros::object
  :slots ())

(setf (get exercise2::move :md5sum-) "e107a27f216b950369e7480afd9738c6")
(setf (get exercise2::move :datatype-) "exercise2/move")
(setf (get exercise2::move :request) exercise2::moveRequest)
(setf (get exercise2::move :response) exercise2::moveResponse)

(defmethod exercise2::moveRequest
  (:response () (instance exercise2::moveResponse :init)))

(setf (get exercise2::moveRequest :md5sum-) "e107a27f216b950369e7480afd9738c6")
(setf (get exercise2::moveRequest :datatype-) "exercise2/moveRequest")
(setf (get exercise2::moveRequest :definition-)
      "string shape
int32 time
---
string lastShape

")

(setf (get exercise2::moveResponse :md5sum-) "e107a27f216b950369e7480afd9738c6")
(setf (get exercise2::moveResponse :datatype-) "exercise2/moveResponse")
(setf (get exercise2::moveResponse :definition-)
      "string shape
int32 time
---
string lastShape

")



(provide :exercise2/move "e107a27f216b950369e7480afd9738c6")


