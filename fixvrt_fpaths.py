import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Fix Paths in VRTs')
parser.add_argument('-d', action="store", dest='fdir', default='./')


args = parser.parse_args()
fdir = Path(args.fdir)

for fxml in fdir.glob('*.vrt'):
    with open(fxml, 'rb') as xml_fp:
        tree = ET.parse(xml_fp)
        root = tree.getroot()
        for src in root.findall("VRTRasterBand"):
            for srcb in src.findall("SimpleSource"):
                print(srcb)
                pfield = srcb.find("SourceFilename")
                imgp = (pfield.text).replace("\\", "/")
                pfield.text = imgp
                if not Path(imgp).is_file():
                    print("{} not found!".format(imgp))
                pfield.text = imgp
    with open(fxml, 'wb+') as dst_xml:
        tree.write(dst_xml)
