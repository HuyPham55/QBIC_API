from API.services.colordescriptor import ColorDescriptor

import argparse
import glob
import cv2

from API.models import Image


def index(imageCollection):
    # 1
    # construct the argument parser and parse the arguments

    # initialize the color descriptor

    # 8 Hue bins, 12 Saturation bins, and 3 Value bins
    cd = ColorDescriptor((8, 12, 3))

    # 2

    # open the output index file for writing
    output = open('index.csv', "w")

    # use glob to grab the image paths and loop over them

    # for item in imageCollection:
    for item in [imageCollection]:
        # extract the image ID (i.e. the unique filename) from the image
        # path and load the image itself

        image = item['content']
        # describe the image
        features = cd.describe(image)

        # write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (item['id'], ",".join(features)))
    # close the index file
    output.close()


def indexFromFolder():
    cd = ColorDescriptor((8, 12, 3))
    output = open('index.csv', "w")
    for imagePath in glob.glob('dataset' + "/*.jpg"):
        # extract the image ID (i.e. the unique filename) from the image
        # path and load the image itself
        imageID = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)


        f = open(imagePath, "rb")
        byte = f.read()
        model = Image(content = byte)
        model.save()

        # describe the image
        features = cd.describe(image)
        # write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (model.id, ",".join(features)))
    output.close()


