call conda activate Py3Dev 
setlocal enabledelayedexpansion
for %%f in (*.tif) do (
    gdal_translate -co compress=zstd -co predictor=2 -co tiled=yes %%f %%~nf.tiff
    if !errorlevel! neq 0 (exit /b !errorlevel!)
    del %%f
    ren %%~nf.tiff %%~nf.tif
)
@pause
