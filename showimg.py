from dashboard.models import DataCamera
from django.db import connections
from datetime import date
import base64, io, time
from PIL import Image, ImageFile

def showimg():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    image = []
    pi = DataCamera.objects.raw('SELECT id,image FROM dashboard_datacamera ORDER BY id DESC LIMIT 0, 3')
    for p in pi:
        image.append(p.image)

    # Decode the string
    binary_data = base64.b64decode(image[0])
    binary_data1 = base64.b64decode(image[1])
    binary_data2 = base64.b64decode(image[2])
    # Convert the bytes into a PIL image
    image = Image.open(io.BytesIO(binary_data))
    image1 = Image.open(io.BytesIO(binary_data1))
    image2 = Image.open(io.BytesIO(binary_data2))

    # Display the image
    image.save('dashboard/static/dashboard/img/1.jpg')
    time.sleep(1)
    image1.save("dashboard/static/dashboard/img/2.jpg")
    time.sleep(1)
    image2.save("dashboard/static/dashboard/img/3.jpg")
    time.sleep(1)
    return "Load picture success!!"