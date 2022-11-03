from API.services.colordescriptor import ColorDescriptor
from API.services.searcher import Searcher
import argparse
import cv2
# 1 

# construct the argument parser and parse the arguments

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))


# 2
def search(query_image):
    # load the query image and describe it
    query = query_image
    features = cd.describe(query)
    # perform the search
    searcher = Searcher("index.csv")
    results = searcher.search(features)
    # loop over the results
    data = []
    for (score, resultID) in results:
        # load the result image and display it
        data.append(resultID)
    return data