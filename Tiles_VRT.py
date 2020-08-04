import gdal
import numpy as np
from math import ceil
from tqdm import tqdm
import rasterio as rio
from pathlib import Path
from itertools import product
from rasterio.enums import ColorInterp
from rasterio import windows as windows

src_dir = Path()
vrt_dir = Path()
dst_dir = Path(r"Tiles")
tile_height = 3000
tile_width = 3000

def generate_windows(img_width, img_height, width, height):
    wins = list()        
    offsets = product(range(0, img_width, width), range(0, img_height, height))
    indices = product(range(0, ceil(img_width / width)), range(0, ceil(img_height / height)))
    big_window = windows.Window(col_off=0, row_off=0, width=img_width, height=img_height)
    for (j, i), (col_off, row_off) in zip(indices, offsets):
        window = windows.Window(
            col_off=col_off,
            row_off=row_off,
            width=width,
            height=height
        )
        win = window.intersection(big_window)
        wins.append(((j, i), win))
    return wins

for imf in tqdm(list(src_dir.glob('*.tif'))):
    tile_list = list()
    vrt_path = vrt_dir / '.'.join([imf.stem, 'vrt'])
    with rio.open(imf, 'r') as src:
        meta = src.meta.copy()
        ih, iw = meta['height'], meta['width']
        wins = generate_windows(img_width=iw, img_height=ih, width=tile_width, height=tile_height)
        transforms = [src.window_transform(win) for _, win in wins]
        geo_windows = list(zip(wins, transforms))
        for ((j, i), w), t in tqdm(geo_windows):
            img_array = src.read(window=w)
            meta['count'], meta['height'], meta['width'] = img_array.shape
            meta['transform'] = t
            meta['compress'] = 'LZW'
            meta['tiled'] = True
            dst_path = dst_dir / ('_'.join([imf.stem, str(i), str(j)]) + imf.suffix)
            with rio.open(dst_path, 'w', **meta) as dst: 
                dst.colorinterp = [
                    ColorInterp.undefined ,
                    ColorInterp.blue,
                    ColorInterp.green, 
                    ColorInterp.red,   
                    ColorInterp.undefined 
                ]
                dst.write(img_array)
            tile_list.append(str(dst_path))
        vrt_options = gdal.BuildVRTOptions(resampleAlg='near', addAlpha=True)
        gdal.BuildVRT(str(vrt_path), tile_list, options=vrt_options)
    imf.unlink()
