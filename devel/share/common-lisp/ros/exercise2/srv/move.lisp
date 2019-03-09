; Auto-generated. Do not edit!


(cl:in-package exercise2-srv)


;//! \htmlinclude move-request.msg.html

(cl:defclass <move-request> (roslisp-msg-protocol:ros-message)
  ((shape
    :reader shape
    :initarg :shape
    :type cl:string
    :initform "")
   (time
    :reader time
    :initarg :time
    :type cl:integer
    :initform 0))
)

(cl:defclass move-request (<move-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <move-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'move-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name exercise2-srv:<move-request> is deprecated: use exercise2-srv:move-request instead.")))

(cl:ensure-generic-function 'shape-val :lambda-list '(m))
(cl:defmethod shape-val ((m <move-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader exercise2-srv:shape-val is deprecated.  Use exercise2-srv:shape instead.")
  (shape m))

(cl:ensure-generic-function 'time-val :lambda-list '(m))
(cl:defmethod time-val ((m <move-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader exercise2-srv:time-val is deprecated.  Use exercise2-srv:time instead.")
  (time m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <move-request>) ostream)
  "Serializes a message object of type '<move-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'shape))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'shape))
  (cl:let* ((signed (cl:slot-value msg 'time)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <move-request>) istream)
  "Deserializes a message object of type '<move-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'shape) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'shape) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'time) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<move-request>)))
  "Returns string type for a service object of type '<move-request>"
  "exercise2/moveRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'move-request)))
  "Returns string type for a service object of type 'move-request"
  "exercise2/moveRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<move-request>)))
  "Returns md5sum for a message object of type '<move-request>"
  "e107a27f216b950369e7480afd9738c6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'move-request)))
  "Returns md5sum for a message object of type 'move-request"
  "e107a27f216b950369e7480afd9738c6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<move-request>)))
  "Returns full string definition for message of type '<move-request>"
  (cl:format cl:nil "string shape~%int32 time~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'move-request)))
  "Returns full string definition for message of type 'move-request"
  (cl:format cl:nil "string shape~%int32 time~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <move-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'shape))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <move-request>))
  "Converts a ROS message object to a list"
  (cl:list 'move-request
    (cl:cons ':shape (shape msg))
    (cl:cons ':time (time msg))
))
;//! \htmlinclude move-response.msg.html

(cl:defclass <move-response> (roslisp-msg-protocol:ros-message)
  ((lastShape
    :reader lastShape
    :initarg :lastShape
    :type cl:string
    :initform ""))
)

(cl:defclass move-response (<move-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <move-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'move-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name exercise2-srv:<move-response> is deprecated: use exercise2-srv:move-response instead.")))

(cl:ensure-generic-function 'lastShape-val :lambda-list '(m))
(cl:defmethod lastShape-val ((m <move-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader exercise2-srv:lastShape-val is deprecated.  Use exercise2-srv:lastShape instead.")
  (lastShape m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <move-response>) ostream)
  "Serializes a message object of type '<move-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'lastShape))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'lastShape))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <move-response>) istream)
  "Deserializes a message object of type '<move-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'lastShape) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'lastShape) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<move-response>)))
  "Returns string type for a service object of type '<move-response>"
  "exercise2/moveResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'move-response)))
  "Returns string type for a service object of type 'move-response"
  "exercise2/moveResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<move-response>)))
  "Returns md5sum for a message object of type '<move-response>"
  "e107a27f216b950369e7480afd9738c6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'move-response)))
  "Returns md5sum for a message object of type 'move-response"
  "e107a27f216b950369e7480afd9738c6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<move-response>)))
  "Returns full string definition for message of type '<move-response>"
  (cl:format cl:nil "string lastShape~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'move-response)))
  "Returns full string definition for message of type 'move-response"
  (cl:format cl:nil "string lastShape~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <move-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'lastShape))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <move-response>))
  "Converts a ROS message object to a list"
  (cl:list 'move-response
    (cl:cons ':lastShape (lastShape msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'move)))
  'move-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'move)))
  'move-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'move)))
  "Returns string type for a service object of type '<move>"
  "exercise2/move")