from pathlib import Path
import rasterio as rio
from tqdm import tqdm

img_dir = Path()
for imf in tqdm(list(img_dir.glob('*.tif'))):
    with rio.open(imf, 'r+') as src:
        assert src.count == 1
        src.write_colormap(
            1,
            {
                0: (0, 0, 0 , 0),
                1: (255, 255, 255 , 255),
                2: (0, 0, 255 , 255),
                3: (0, 255, 255 , 255),
                4: (0, 255, 0 , 255),
                5: (255, 255, 0 , 255),
                6: (255, 0, 0 , 255)
            }
        )
