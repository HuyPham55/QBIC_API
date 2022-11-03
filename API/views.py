from django.shortcuts import render
# Create your views here.
from API.models import Image
import cv2
import numpy
import base64


from API.services.colordescriptor import ColorDescriptor

from django.http import HttpResponse

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

def writeToFile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def saveFileToDatabase():
    # where r = reading, b = binary
    # https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
    f = open("dataset/IMG_20221025_160840.jpg", "rb")
    image = f.read()
    model = Image.objects.get(id = 2)
    model.content = image
    model.save()


def saveDatabaseToFile():
    # works with saveFileToDatabase
    model = Image.objects.get(id = 2)
    byteData = model.content
    writeToFile(byteData, "Saved.jpg")
def convertDatabaseToBase64():
    model = Image.objects.get(id = 2)
    byteData = model.content
    base64EncodedStr = base64.b64encode(byteData)
    # https://bobbyhadz.com/blog/python-typeerror-can-only-concatenate-str-not-bytes-to-str
    return base64EncodedStr.decode('utf-8')

def convertBase64ToByte(string):
    return base64.b64decode(string)

def openImageFromDatabaseWithOpenCV():
    model = Image.objects.get(id = 2)
    byteData = model.content
    np_arr = numpy.fromstring(byteData, numpy.uint8)
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR )
    # https://stackoverflow.com/questions/17170752/python-opencv-load-image-from-byte-string
    return img_np
    cv2.imshow("RESULT", img_np)
    cv2.waitKey(0)

def index(request):
    base64 = convertDatabaseToBase64()
    openImageFromDatabaseWithOpenCV()

    query = openImageFromDatabaseWithOpenCV()
    features = cd.describe(query)
    print(features)

#     image = numpy.asarray(bytearray(byteData), dtype="uint8")
#     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#     cv2.imwrite("result.jpg", image)
    return HttpResponse("<img src='data:image/jpeg;base64,"+base64+"'/>")


def search(request):
    if request.method == "POST":
        data = request.POST
        return HttpResponse("OK")