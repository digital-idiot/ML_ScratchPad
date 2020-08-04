 #!/bin/sh
 source activate Py3Dev
 
 for fin in *.tif
 do
    fout=${fin%.*}.tiff
    gdal_translate -co compress=lzw -co predictor=2 -co tiled=yes $fin $fout
    if [ $? -ne 0 ]
    then
        exit -1
    rm $fin
    mv $fout $fin
done
