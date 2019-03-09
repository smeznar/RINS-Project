
(cl:in-package :asdf)

(defsystem "exercise2-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "move" :depends-on ("_package_move"))
    (:file "_package_move" :depends-on ("_package"))
  ))