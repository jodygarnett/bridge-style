import os
import argparse
import shutil

from . import sld
from . import geostyler
from . import mapboxgl
from . import arcgis

_exts = {"sld": sld, "geostyler": geostyler, "mapbox": mapboxgl, "lyrx": arcgis}


def convert(fileA, fileB, options):
    extA = os.path.splitext(fileA)[1][1:]
    extB = os.path.splitext(fileB)[1][1:]
    if extA not in _exts:
        print("Unsupported style type: '%s'" % extA)
        return
    if extB not in _exts:
        print("Unsupported style type: '%s'" % extB)
        return

    with open(fileA) as f:
        styleA = f.read()

    geostyler, icons, geostylerwarnings = _exts[extA].toGeostyler(styleA, options)
    styleB, warningsB = _exts[extB].fromGeostyler(geostyler, options)
    outputfolder = os.path.dirname(fileB)
    for f in icons:
        dst = os.path.join(outputfolder, os.path.basename(f))
        shutil.copy(f, dst)
    for w in geostylerwarnings + warningsB:
        print(f"WARNING: {w}")

    with open(fileB, "w") as f:
        f.write(styleB)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true',
                        help="Convert attribute names to lower case",
                        dest="tolowercase")
    parser.add_argument('-e', action='store_true',
                        help="Replace Esri font markers with standard symbols",
                        dest="replaceesri")
    parser.add_argument('src')
    parser.add_argument('dst')
    args = parser.parse_args()

    argsdict = dict(vars(args))
    del argsdict["src"]
    del argsdict["dst"]
    convert(args.src, args.dst, argsdict)
