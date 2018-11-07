@echo off
set CAM_CALIB_DIR=%~dp0
call %CAM_CALIB_DIR%config.ini
set SUOSTITCH_DIR=C:\Users\demoPC\Desktop\SuoStitch_v2.6.0\
set OUTPUT_DIR=%CAM_CALIB_DIR%\output_ids\output_%METHOD%\

move %SUOSTITCH_DIR%\bin\out.avi %OUTPUT_DIR%\out_%METHOD%.avi
echo stitching complete.. avi created in the output directory

rem convert the AVI to PNGs.. group them in a folder
python avi2png.py -p %OUTPUT_DIR%\ -f *.avi 
rem out_%METHOD%.avi
echo avi2png conversion complete

rem run depth calculation on the batch of images
mkdir %OUTPUT_DIR%\plot
python estimate_depth.py -s %OUTPUT_DIR%\ -d %OUTPUT_DIR%\plot\
copy output.txt %OUTPUT_DIR%\output_%METHOD%.txt
echo output file generated in folder %OUTPUT_DIR%

pause
goto end

rem run data frame analysis to generate goodness of model
python dataframe_analysis_model.py -f %OUTPUT_DIR%\output_%METHOD%.txt

:end
