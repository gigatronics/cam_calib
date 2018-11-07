goto start_here

@echo off
set CAM_CALIB_DIR=%~dp0
set OUTPUT_DIR=%CAM_CALIB_DIR%\output_ids\
set SUOSTITCH_DIR=C:\Users\demoPC\Desktop\SuoStitch_v2.6.0\
call %CAM_CALIB_DIR%config.ini

echo %METHOD%
mkdir %OUTPUT_DIR%\output_%METHOD%

cp IMG_PATH\*.avi SUOSTITCH_DIR\*.avi
cp MODEL_DIR\*.txt SUOSTITCH_DIR\*.txt



set METHOD=_test
mkdir folder_%METHOD%



python avi2png.py -p .\output_ids\ -f out_ext_2m.avi
echo avi2png conversion complete
pause

:start_here 

python estimate_depth.py -s C:\Users\demoPC\py\cam_calib\output_ids\
pause
