from django.shortcuts import render
# Create your views here.
import cv2
import numpy
import base64
import json

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse

from django.http import JsonResponse

from django.core import serializers

from API.services.index import index as serviceIndex

from API.models import Image

from API.services.colordescriptor import ColorDescriptor

from API.services.search import search as serviceSearch

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

def convertByteToImage(byteData):
    # Return OpenCV compatible image
    np_arr = numpy.fromstring(byteData, numpy.uint8)
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR )
    # https://stackoverflow.com/questions/17170752/python-opencv-load-image-from-byte-string
    return img_np

def convertByteToBase64(byteData):
    base64EncodedStr = base64.b64encode(byteData)
    # https://bobbyhadz.com/blog/python-typeerror-can-only-concatenate-str-not-bytes-to-str
    return base64EncodedStr.decode('utf-8')

def convertBase64ToByte(string):
    return base64.b64decode(string)

def reIndex():
    data = []
    for item in Image.objects.all():
        data.append({'id': item.id, 'content': convertByteToImage(item.content)})
    serviceIndex(data)

@csrf_exempt
def index(request):
    collection = Image.objects.all()
    data = []
    for item in collection:
        data.append({'id': item.id, 'content': convertByteToBase64(item.content)})
    return JsonResponse(data, safe=False)

@csrf_exempt
def search(request):
    if request.method == "POST":
        data = request.POST
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']
        byteData = convertBase64ToByte(content)
        image = convertByteToImage(byteData)
        results = serviceSearch(image)
        response = []
        for id in results:
            model = Image.objects.get(id = id)
            base64 = convertByteToBase64(model.content)
            response.append({'id': id, 'content': base64})
        return JsonResponse(response, safe = False)
    return HttpResponse("OK")

@csrf_exempt
def add(request):
    if request.method == "POST":
        data = request.POST
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']
        byteData = convertBase64ToByte(content)
        model = Image(content = byteData)
        model.save()

        reIndex()
        return JsonResponse({'status': 'OK'}, status = 200)
    return HttpResponse("OK")

@csrf_exempt
def delete(request):
    if request.method == "POST":
        data = request.POST
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id = body['id']
        Image.objects.filter(id = id).delete()

        reIndex()
        return JsonResponse({'status': 'OK'}, status = 200)
    return HttpResponse("OK")




def saveFileToDatabase(): #unused
    # where r = reading, b = binary
    # https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
    f = open("dataset/IMG_20221025_160840.jpg", "rb")
    image = f.read()
    model = Image.objects.get(id = 2)
    model.content = image
    model.save()


