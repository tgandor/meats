;; simple hello world script, Alan Horkan 2004
;; so long as remove these comments from your script
;; feel free to use it for whatever you like.  

(define (script-fu-hello-world)
    (gimp-message "Hello World")
)

(script-fu-register "script-fu-hello-world"
    _"<Image>/Script-Fu/Test/Hello World"
    "Hello World, the simplest example I could think of shows a Warning Message.  
Feel free to use this as a script template"
    "Author Name goes here.  " ; author
    "Public Domain.  No Copyright.  " ; copyright information  
    "April 2004" ; date 
    "*" ; image types
    SF-IMAGE "Image" 0
    SF-DRAWABLE "Drawable" 0
)
