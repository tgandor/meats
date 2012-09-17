
(define (unpack vars vals)
  "Pair two lists... Not working for my purpose! Equivalent to (map list vars vals)"
  (if (null? vars)
    '()
    (cons (list (car vars) (car vals)) (unpack (cdr vars) (cdr vals)) )
  )
)

(define (join-nums nums)
  "Join integers into a string separated by spaces."
  (let* ( 
      (spaces        (make-list (length nums) " "))
      (nums-stringed (map number->string nums))
      (nums-spaced   (map string-append spaces nums-stringed))
    )
    (eval (cons string-append nums-spaced))
  )
)

(define (script-fu-snap-portrait image layer)
    (let* ( 
        (selection (gimp-selection-bounds image)) 
      )
      (if (equal? (car selection) 1)
        (let* 
          (
               (x1 (cadr selection))
               (y1 (caddr selection))
               (x2 (cadddr selection))
               (y2 (car (cddddr selection)))
               (xsize (- x2 x1))
               (ysize (- y2 y1))
          )
          ;(if (> ysize (* xsize 0.75))
             (set! ysize (/ xsize 0.75))
          ;   (set! xsize (* ysize 0.75))
          ;)
	  (gimp-rect-select image x1 y1 xsize ysize 2 FALSE 0.0)
          (gimp-message (string-append 
            "Selection cut down to " 
            (number->string xsize)
            " x "
            (number->string ysize)
            " px."
          ))
        )
        (gimp-message "Selection absent")
      )
      ; (gimp-message (string-append "Selection present " (number->string (car selection))))
      ; (gimp-message (string-append "Selection present " (join-nums selection)))
   )
)

(script-fu-register "script-fu-snap-portrait"
    _"<Image>/Script-Fu/Snap Portrait"
    "Reduce the selection to be 3x4 portrait proportions"
    "Tomasz Gandor" ; author
    "GPLv3" ; copyright information  
    "August 2009" ; date 
    "*" ; image types
    SF-IMAGE "Image" 0
    SF-DRAWABLE "Drawable" 0
)

(define (script-fu-snap-landscape image layer)
    (let* ( 
        (selection (gimp-selection-bounds image)) 
      )
      (if (equal? (car selection) 1)
        (let* 
          (
               (x1 (cadr selection))
               (y1 (caddr selection))
               (x2 (cadddr selection))
               (y2 (car (cddddr selection)))
               (xsize (- x2 x1))
               (ysize (- y2 y1))
          )
          ; (if (> xsize (* ysize 0.75))
          ;   (set! xsize (/ ysize 0.75))
             (set! ysize (* xsize 0.75))
          ;)
	  (gimp-rect-select image x1 y1 xsize ysize 2 FALSE 0.0)
          (gimp-message (string-append 
            "Selection cut down to " 
            (number->string xsize)
            " x "
            (number->string ysize)
            " px."
          ))
        )
        (gimp-message "Selection absent")
      )
      ; (gimp-message (string-append "Selection present " (number->string (car selection))))
      ; (gimp-message (string-append "Selection present " (join-nums selection)))
   )
)

(script-fu-register "script-fu-snap-landscape"
    _"<Image>/Script-Fu/Snap Landscape"
    "Reduce the selection to be 3x4 landscape proportions"
    "Tomasz Gandor" ; author
    "GPLv3" ; copyright information  
    "August 2009" ; date 
    "*" ; image types
    SF-IMAGE "Image" 0
    SF-DRAWABLE "Drawable" 0
)
