import cv2
from django.shortcuts import render
from django.http import JsonResponse
from binascii import a2b_base64
from . import load_model
from torchvision import transforms
import numpy as np
# Create your views here
def index(request):
    return render(request, 'index.html')

def MNIST(request):
    return render(request, 'mnist.html')

def save_drawing(request):
    if request.method == 'POST':
        drawing_data = request.POST.get('data')
        img = drawing_data.replace(' ', '+')
        img = img.split('"')
        img = img[3]
        img = img.split(',')[1]
        img = a2b_base64(img)

        f = open('image.png','wb')
        f.write(img)
        f.close()

        transform = transforms.Compose([
            transforms.ToTensor()
        ])
        model, loss = load_model.model_loader()
        img = cv2.imread('image.png')
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = (255 - img)
        img = cv2.resize(img, (28, 28))
        img_s = cv2.dilate(img, (20, 20), iterations=1)
        img = np.array([[0 if y < 127 else 255 for y in x] for x in img_s], dtype='float32')
        # cv2.imshow('a', img)
        # cv2.waitKey(0)
        img = transform(img)
        pred = model(img.unsqueeze(0)).detach().tolist()[0]
        print(pred)

        # Optionally, you can return a response to the client
        return JsonResponse({'message': pred.index(max(pred))})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def test2(request):
    return render(request,'test2.html')