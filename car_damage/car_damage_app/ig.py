from image_transforms import transforms as tsfms
import glob
import argparse
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
# from src.nnmodules.resnet import get_model
from PIL import Image
from skimage import io, filters, morphology as morph, transform
from skimage.morphology import disk, square
from sklearn import metrics
from torch.autograd import Variable as var
from torchvision.transforms import Compose
import numpy as np
import progressbar
from shutil import copyfile, move
import os
import visdom
import math
import sys
from .utils import conv_averaged, merge_image_heatmap

def ig_iter(im, base, steps):
    dif_im = im - base
    for i in range(0, steps):
        yield base + i*(dif_im)/(steps-1)


def smooth_ig(im, model, base, steps=80, samples=10):
    boo, smooth_map = ig_grad(im, model, base, steps)
    if samples > 0:
        for sample in add_noise(im, samples):
            tup = ig_grad(sample, model, base, steps)
            if tup[0]:
                smooth_map += tup[1]
            else:
                return (False, None)
    if boo:
        return (True, smooth_map/(samples+1))
    else:
        return (False, None)

def ig_grad(im, model, base, steps=50):

    try:
        print(pim(im).size)
        score = F.softmax(model.forward(pim(im)))
        print(score[0][1].data.cpu())
        sc = score[0][1].data.cpu()[0]
        if sc < 1:
            sample_batch, step = gen_ten(im, base, steps)
            sample_batch = var(sample_batch.data, requires_grad=True)
            sample_out = F.softmax(model.forward(sample_batch))
            crit = get_crit()
            sample_loss = crit(sample_out, var(torch.ones((steps)).long().cuda()))
            sample_loss.backward()
            sample_grad = sample_batch.grad*step
            return (True, sample_grad.sum(0))
        else:
            return (False, None)
    except Exception as e:
        print(e)
#         return (False, None)

def get_crit():
    crit = nn.CrossEntropyLoss(torch.Tensor([1, 10]))
    return crit.cuda()

def add_noise(im, steps=30):
    if steps == 0:
        yield im
    std = im.max()*0.15
    for i in range(0, steps):
        noise = torch.Tensor(pim(im).data[0][0].size()).normal_(0.0, std)
        yield im+noise.numpy()#var(noise.cuda())

def pim(im):
    val_tfm = Compose([
    tsfms.Resize(256),
    tsfms.CenterCrop(256),
    tsfms.Normalize((0.48, 0.225), mode='meanstd'),
    tsfms.ToTensor()
    ])
    imt = val_tfm(im)
    imb = imt.unsqueeze(0)
    imb = var(imb.cuda(), requires_grad=True)
    return imb

def norm(im):
    im = im- im.mean()
    im = im/(im.std()+0.000001)
    return im

def scale(im):
    im = im- im.min()
    im = im/(im.max()+0.000001)
    return im

def _load_model(mpath):
    m = torch.load(mpath)
    sd = m['network']
    args = m['args']
    args.resnet_depth=18
    model = get_model(args)
    model.load_state_dict(sd)
    model = model.eval().cuda()
    return model

def gen_ten(im, base, steps):
    step = (im - base)/steps
    ten_lis = [pim(x) for x in ig_iter(im, base, steps)]
    final_ten = torch.cat(tuple(ten_lis), 0)
    return final_ten, pim(step[0]).repeat(steps,1,1,1)


def smooth_average(hmap, iters=2, ker=11):
    smap = hmap
    print(hmap.shape)
    for i in range(0, iters):
        smap = conv_averaged(smap, ker)
    return smap

def to3(im):
    new_im = np.expand_dims(im, 0)
    new_im = np.repeat(new_im, 3, axis =0)
    new_im = np.transpose(new_im, (1,2,0))
    return scale(new_im)

def tt(arr):
    tfm = Compose([
        tsfms.ToTensor()
    ])
    return tfm(arr)


def get_hmaps(im, base, model):
    tup = smooth_ig(im , model, scale(base), 100, 0)
    ig = tup[1]
    if tup[0]:
        hmap = scale(ig.data[0].cpu().numpy())
        new_hmap = smooth_average(hmap, 4, 7)
        new_hmap = scale(new_hmap)
        return new_hmap
    else:
        return None
