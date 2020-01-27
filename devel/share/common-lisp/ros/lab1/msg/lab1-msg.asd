
(cl:in-package :asdf)

(defsystem "lab1-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Gps_data" :depends-on ("_package_Gps_data"))
    (:file "_package_Gps_data" :depends-on ("_package"))
  ))