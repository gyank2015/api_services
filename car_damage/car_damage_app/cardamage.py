from __future__ import absolute_import

import torch
from torch.autograd import Variable
from PIL import Image

import torch.nn as nn
from torchvision import transforms as tsfms
from torchvision import models, datasets
import numpy as np
from .deeplabv3 import DeeplabV3
from collections import Counter

import scipy.misc as scm
from .ig import get_hmaps
from .utils import merge_image_heatmap
from skimage import transform
import os
from avengers_django_models_app.models import uploadedImages, resultTable
from django.conf import settings
# from .serializers import txnID_fileHash

def carpart_damage_analysis(filename):

        # image_pil = Image.open('uploads/{}'.format(filename))
        filepath = os.path.abspath(os.path.join(settings.ABS_MEDIA_ROOT, 'upload_service/' + filename))
        print(filepath)
        # filepath = os.path.abspath('/fractal/home/gyan/avengers/media/{}'.format(filename))
        image1 = scm.imread(filepath)
        # transform_val = tsfms.Scale((256, 256))
        #h, w = np.shape(image)[0], np.shape(image)[1]
        image = transforms1(image1, 256)
        image2 = transforms1(image1, 256)
        
        #transform_save = tsfms.Scale((h, w))
        
        #image1 = transform_save(image)
        scm.imsave('image.png', image)
        # scm.imsave('imagex.png',image2)
        
        image = np.expand_dims(image, axis=0)
        image = np.swapaxes(image, 1, 3)
        image = torch.from_numpy(image)
        image = image.float()
        checkpoint = torch.load(os.path.join(settings.DL_MODELS_ROOT, 'classifier.pth'),map_location=lambda storage, loc: storage)
        #checkpoint = torch.load("trained_models/classifier.pth", map_location=lambda storage, loc: storage)
        # checkpoint = torch.load("/fractal/home/gyan/avengers/trained_models/classifier.pth")

        classfier_model = models.resnet18(pretrained=True)
        classfier_model.avgpool = nn.AdaptiveAvgPool2d(1)

        num_ftrs = classfier_model.fc.in_features

        classfier_model.fc = nn.Linear(num_ftrs, 2)
        classfier_model.load_state_dict(checkpoint)
        classfier_model.eval()

        if torch.cuda.is_available():
            classfier_model.cuda()
            image = Variable(image.cuda())
        else:
            image = Variable(image)
        # Heat map generation code
        base = np.zeros(np.shape(image1))
        im = get_hmaps(image1, base, classfier_model)
        output = merge_image_heatmap(image2, im, 0.8)
        damaged_pixels  = np.argwhere(im >0.85)
        # scm.imsave('uploads/heatmap_{}.png'.format(filename.split('.')[0]), output)
        print(os.path.join(settings.PROJ_MEDIA_ROOT,'heatmap/',filename))
        # print("%%%%%")
        scm.imsave(os.path.join(settings.PROJ_MEDIA_ROOT,'heat_map/',filename), output)

        # Classifier output
        outputs_classifier = classfier_model(image)
        pred_classifier = np.squeeze(outputs_classifier.data.max(1)[1].cpu().numpy(), axis=0) 


        model = DeeplabV3(14)
        # model_dict = torch.load("trained_models/carpart.pth", map_location=lambda storage, loc: storage)
        model_dict = torch.load(os.path.join(settings.DL_MODELS_ROOT,'carpart.pth'),map_location=lambda storage, loc: storage)
        model.load_state_dict(model_dict)
        model.eval()

        if torch.cuda.is_available():
            model.cuda()
            #image = Variable(image.cuda())
        else:
            image3 = Variable(image)
        

        # Segmentation output      
        outputs = model(image)
        pred = outputs[0].data.cpu().numpy()
                
        pred = np.argmax(pred, axis=0)
        #pred = np.sum(pred,axis = 2)
        r = pred.copy()
        g = pred.copy()
        b = pred.copy()
        parts_vals = np.unique(pred)
        parts_list = [
                    "background",
                    "back_license_plate",
                    "rear_side",
                    "door",
                    "front_license_plate",
                    "front_side",
                    "headlight",
                    "left_mirror",
                    "left_side",
                    "right_mirror",
                    "right_side",
                    "roof_side",
                    "wheel",
                    "window"
    	           ]
        damaged_parts = []
        if pred_classifier == 0:
            for pixel in damaged_pixels.tolist():
                damaged_parts.append(parts_list[pred[pixel[0],pixel[1]]])
        damaged_parts = set(damaged_parts)
        print(damaged_parts)
        parts_found = {}
        for i, part in enumerate(parts_list):
            if i != 0:
                if i in parts_vals.tolist():
                    parts_found[part] = "YES"
                else:
                    parts_found[part] = "NO"
        damaged_parts_dict = {}
        for part in parts_list:
            print(part)
            if part in damaged_parts:
                damaged_parts_dict[part] = "DAMAGED"
            else:
                damaged_parts_dict[part] = "UN-DAMAGED"

        heat_map_image_path={'heat_map_image_path':""}
        segmentation_image_path={'segmentation_image_path':""}
        imagehash={'imageID':filename.split(".")[0]}
        heat_map_image_path['heat_map_image_path']+=(os.path.join(settings.PROJ_MEDIA_ROOT,'heatmap/',filename))
        label_colours = np.asarray([[0,0,0], [51,0,0], [255,153,51], [51,51,0], [64,64,64], [204,0,102],
                                          [204,255,204], [0,204,204], [0,51,51], [255,153,153], [0,0,51], [255,204,204],
                                                                        [64,0,128],[0, 76,153]])
        for l in range(14):
            r[pred == l] = label_colours[l, 0]
            g[pred == l] = label_colours[l, 1]
            b[pred == l] = label_colours[l, 2]

        rgb = np.zeros((pred.shape[0], pred.shape[1], 3))
        rgb[:, :, 0] = r
        rgb[:, :, 1] = g
        rgb[:, :, 2] = b
        filename=filename.split(".")[0]+'.png'
        scm.imsave(os.path.join(settings.PROJ_MEDIA_ROOT, 'segmentation/',filename), rgb, 'png')
        # print(damaged_parts_dict)
        segmentation_image_path['segmentation_image_path']+=(os.path.join(settings.PROJ_MEDIA_ROOT, 'segmentation/',filename))
        return imagehash, parts_found, damaged_parts_dict , heat_map_image_path, segmentation_image_path


def transforms1(image, size):
    h, w = np.shape(image)[0], np.shape(image)[1]
    print(h, w)
    if h > w:
        output_shape = (int(h * size/w), size)
        # if (size - int(w*size/h) % 2) == 1:
        #     pad_left = (size - int(w*size/h)) // 2
        #     pad_right = (size - int(w *size/h)) // 2 + 1
        #     pad_top = 0
        #     pad_bottom = 0
        # else:
        #     pad_left = (size - int(w*size/h)) // 2
        #     pad_right = (size - int(w*size/h)) // 2
        #     pad_top = 0
        #     pad_bottom = 0
    else:
        output_shape = (size, int(w*size/h))
        # if (size - int(h*size/w) % 2) == 1:
        #     pad_top = (size - int(h*size/w)) // 2
        #     pad_bottom = (size - int(h *size/w)) // 2 + 1
        #     pad_left = 0
        #     pad_right = 0
        # else:
        #     pad_top = (size - int(h*size/w)) // 2
        #     pad_bottom = (size - int(h*size/w)) // 2
        #     pad_left = 0
        #     pad_right = 0

    image = transform.resize(image, output_shape)
    
    # image = image * 255.0
    # image = Image.fromarray((image).astype('uint8'))

    # image.save('random.png')
    # print(pad_left, pad_top, pad_right, pad_bottom)
    # trans = tsfms.Pad((pad_left, pad_top, pad_right, pad_bottom))
    # image = trans(image)
    new_h, new_w = size, size
    h1, w1 = (np.shape(image)[0] - new_h) // 2, (np.shape(image)[1] - new_w) //2
    return image[h1:h1 + new_h, w1:w1 + new_w]
    
