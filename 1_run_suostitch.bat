goto start_here

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 09:50:50 2018

@author: demoPC


here are the steps to go from frames to goodness of model:

1. a series of frames.. png2avi stitch 10 frames together to avi 
2
3. copy model files and frames to suostitch.. to generate an avi
4. convert the AVI to PNGs.. group them in a folder
5. run depth analysis to 

"""
# import subprocess
# subprocess.call('cmd /c setup.batch')

FRAMES_OUT_DIR = input("enter frames_out path:")
METHOD = input("enter a name for method_under_test:")


:start_here

rem prompt the user to enter data path
rem set /p MODEL_DIR = Enter the model file directory (e.g. C:\Users\demoPC\py\cam_calib\output_model\pert_int):
rem set /p IMG_DIR = Enter the image file directory (e.g. D:\data\frames_out\): 
rem set /p METHOD = Enter a name for the method_under_test (e.g. _int_3m):

REM initial folder setup.. create output_METHOD folder.. dump everything there, seperate later
@echo off
set CAM_CALIB_DIR=%~dp0
call %CAM_CALIB_DIR%config.ini

set SUOSTITCH_DIR=C:\Users\demoPC\Desktop\SuoStitch_v2.6.0\
set OUTPUT_DIR=%CAM_CALIB_DIR%\output_ids\output_%METHOD%\
rem mkdir %OUTPUT_DIR%\output_%METHOD%
rem mkdir %OUTPUT_DIR%\png_%METHOD%

rem a series of frames.. png2avi stitch 10 frames together to avi 

rem copy model files and frames to suostitch.. to generate an avi
xcopy /e/s %IMG_PATH%\*.avi %SUOSTITCH_DIR%\*.avi
xcopy /e/s %MODEL_DIR%\*.txt %SUOSTITCH_DIR%\*.txt
echo copy complete 

rem run suostitch
cd %SUOSTITCH_DIR%\bin
SuoStitch.exe
ren %SUOSTITCH_DIR%\bin\out.avi %SUOSTITCH_DIR%\bin\out_%METHOD%.avi
move %SUOSTITCH_DIR%\bin\out_%METHOD%.avi %OUTPUT_DIR%\out_%METHOD%.avi
echo stitching complete.. avi created in the output directory


rem convert the AVI to PNGs.. group them in a folder
python avi2png.py -p .\output_ids\ -f out_ext_2m.avi
move .\output_ids\*.png %OUTPUT_DIR%\
echo avi2png conversion complete

rem run depth calculation on the batch of images
python estimate_depth.py -s %OUTPUT_DIR%\
move output.txt %OUTPUT_DIR%\output_%METHOD%.txt
echo output file generated

goto end

rem run data frame analysis to generate goodness of model
python dataframe_analysis_model.py -f %OUTPUT_DIR%\output_%METHOD%.txt

:end
