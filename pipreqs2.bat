@rem
@rem call pipreqs with our options .. make sure to use the proper environment
@rem
@pipreqs --mode no-pin --debug --clean requirements.txt
@if %ErrorLevel% equ 0 (echo ok) else (echo Fail)
