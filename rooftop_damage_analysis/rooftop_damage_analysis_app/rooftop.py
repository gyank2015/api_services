from __future__ import absolute_import


import torch
from torch.autograd import Variable
import scipy.misc as scm
from PIL import Image
from torch.utils import data
import numpy as np
from .deeplabv3 import DeeplabV3
from collections import Counter

from skimage import transform
import os

from django.conf import settings


def rooftop_damage_analysis(filename, result_filename):
    filepath = os.path.abspath(os.path.join(settings.ABS_MEDIA_ROOT, 'upload_service/' + filename))
    image = scm.imread(filepath)

    image = transforms(image, 256)

    image = np.expand_dims(image, axis=0)
    image = np.swapaxes(image, 1, 3)
    image = torch.from_numpy(image)
    image = image.float()

    model = DeeplabV3(6)
    model_dict = torch.load(os.path.join(settings.DL_MODELS_ROOT, 'rooftop.pth'),
                            map_location=lambda storage, loc: storage)
    model.load_state_dict(model_dict)
    model.eval()

    if torch.cuda.is_available():
        model.cuda()
        image = Variable(image.cuda())
    else:
        image = Variable(image)
    outputs = model(image)
    pred = outputs[0].data.cpu().numpy()
    # decoded = loader.decode_segmap(pred[0])
    # pred = np.swapaxes(pred,0,2)

    pred = np.argmax(pred, axis=0)

    r = pred.copy()
    g = pred.copy()
    b = pred.copy()

    r[pred == 4] = 153
    r[pred == 4] = 0
    r[pred == 4] = 76

    r[pred == 3] = 255
    g[pred == 3] = 102
    b[pred == 3] = 102

    r[pred == 1] = 102
    g[pred == 1] = 178
    b[pred == 1] = 255

    r[pred == 0] = 192
    g[pred == 0] = 192
    b[pred == 0] = 192

    rgb = np.zeros((pred.shape[0], pred.shape[1], 3))
    rgb[:, :, 0] = r
    rgb[:, :, 1] = g
    rgb[:, :, 2] = b
    scm.imsave(os.path.join(settings.PROJ_MEDIA_ROOT, result_filename), rgb, 'png')

    pixel_values = ["background", "roof", "", "hail damage", "shingle missing", "broken roof"]
    damage_type = []

    unique, counts = np.unique(pred, return_counts=True)

    print(unique)
    print(counts)
    count_dict = dict(zip(unique, counts))
    damage_type = "NONE"
    damage_percentage = 0
    for key in count_dict.keys():
        if key == 3:
            damage_type = "shingle damage"
            damage_percentage = round(count_dict[3] * 100 / float(count_dict[1]), 2)
        elif key == 4:
            damage_type = "Hail damage"
            damage_percentage = round(count_dict[4] * 100 / float(count_dict[1]), 2)

    damage_details = {'damage_type': damage_type, 'damage_percentage': damage_percentage}

    return damage_details


def transforms(image, size):
    h, w = np.shape(image)[0], np.shape(image)[1]
    if h > w:
        output_shape = (int(h * size / w), size)
    else:
        output_shape = (size, int(w * size / h))
    image = transform.resize(image, output_shape)
    new_h, new_w = size, size
    h1, w1 = (np.shape(image)[0] - new_h) // 2, (np.shape(image)[1] - new_w) // 2
    return image[h1:h1 + new_h, w1:w1 + new_w]
