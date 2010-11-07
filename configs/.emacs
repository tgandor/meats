
(setq tab-width 2)

(setq c-basic-offset 2)

;(global-set-key (kbd "C-z") 'shell)    

(defun save-compile-run ()
  "Save compile and execute the file in current buffer."
  (interactive)
  (let (f)
    (setq f (file-name-sans-extension (buffer-name)))
    (save-buffer)
    ;; this is bad - asynchronous
    ;; (compile (concat "make -k " f))
    (shell-command (concat "make -k " f))
    (shell-command (concat "./" f))))

;; (global-set-key (kbd "<f5>") 'save-compile-run)    

(add-hook
 'c++-mode-hook
 '(lambda () (define-key c++-mode-map (kbd "<f5>") 'save-compile-run)))


(defun init-python-file()
  (unless (file-exists-p (buffer-file-name))
    (progn
      (insert "#!/usr/bin/env python")
      (newline)
      (newline)
      (insert "if __name__=='__main__':")
      (newline)
      (insert "    "))))
      
(add-hook 'python-mode-hook 'init-python-file)

;; (add-hook
;;  'c++-mode-hook
;;  '(lambda () (global-set-key (kbd "C-c C-v") 'save-compile-run)))


;; (if (string= major-mode "c++-mode")
;;     (global-set-key (kbd "C-c C-v") 'save-compile-run))

;; (global-set-key (kbd "C-c C-v") 'save-compile-run)

;; (define-key c++-mode-map (kbd "C-c C-v") 'save-compile-run)

(server-start)
