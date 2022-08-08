@rem
@rem call flake8 with our options .. make sure to use the proper environment
@rem
@flake8 --ignore E127,E501,E722,W504 --exclude _vendor
if %ErrorLevel% equ 0 (echo ok) else (echo Fail)
