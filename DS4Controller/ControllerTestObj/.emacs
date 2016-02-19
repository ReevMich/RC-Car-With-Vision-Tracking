;;; my additions  --------------

(define-key global-map "\eg"    'goto-line)     ;; M-g = goto-line
(global-set-key "\C-h" 'delete-backward-char)
(global-set-key "\eh" 'help-for-help)


(setq inhibit-startup-message t)
(setq require-final-newline t)
(setq display-time-day-and-date 1)
(setq line-number-mode t)
(setq column-number-mode t)
(display-time)
(setq scroll-bar-mode-explicit t)
(set-scroll-bar-mode `right)

;; Clean up files when saving
;;(setq write-contents-hooks '(strip-last-space-file))


;; Turn on autofill in text mode files
(setq text-mode-hook
      '(lambda () (auto-fill-mode 1)))

(if window-system
    (progn
      (set-mouse-color "red")
      (set-cursor-color "blue")
      (set-background-color "white")
      (set-default-font "8x13")


      (auto-image-file-mode t)
      )
  )

(setq default-major-mode 'text-mode)



(require 'paren)
;; By an unknown contributor

(global-set-key "%" 'match-paren)

(defun match-paren (arg)
  "Go to the matching parenthesis if on parenthesis otherwise insert %."
  (interactive "p")
  (cond ((looking-at "\\s\(") (forward-list 1) (backward-char 1))
	((looking-at "\\s\)") (forward-char 1) (backward-list 1))
	(t (self-insert-command (or arg 1)))))

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(blink-cursor-mode nil)
 '(case-fold-search t)
 '(column-number-mode t)
 '(current-language-environment "English")
 '(display-time-mode t)
 '(global-font-lock-mode t nil (font-lock))
 '(mouse-wheel-mode t nil (mwheel))
 '(show-paren-mode t nil (paren))
 '(size-indication-mode t)
 '(tool-bar-mode nil))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:inherit nil :stipple nil :background "blue" :foreground "white" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 90 :width normal :foundry "unknown" :family "Liberation Mono")))))

(setq-default c-basic-offset 2)
;;(ess-toggle-underscore nil)
(setq initial-scratch-message nil)

(add-to-list 'auto-mode-alist '("\\.ino\\'" . c++-mode))
(global-linum-mode t)
