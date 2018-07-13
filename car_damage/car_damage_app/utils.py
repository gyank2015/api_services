"""Utilities for heatmap generation."""
import torch
import torch.nn.functional as F
from torch.autograd import Variable

import numpy as np
from PIL import Image
from matplotlib import cm


def merge_image_heatmap(image, heatmap, thresh=0.6, color=(255, 255, 255)):
    """Merge an image and heatmap to create a single image.

    Arguments
    ---------
    image: ndarray
        A H*W*3 array. Must be an RGB image.
    heatmap: ndarray
        A H*W array of probability of each pixel, probability is directly
        proportional to the importance of pixel in outcome.
    color: tuple(int)
        A size 3 tuple of int.

    Returns
    -------
    ndarray
        Numpy aray with heatmap embedded onto image and opacity of 0.25.

    """
    assert image.shape[2] == 3, \
        "Input image has {} channels, must have 3.".format(image.shape[2])
    background = np.concatenate([
        image, np.ones(shape=(heatmap.shape[0], heatmap.shape[1], 1))], axis=2)
    background = np.uint8(background * 255)
    background_image = Image.fromarray(background)
    foreground = np.uint8(cm.jet(heatmap) * 255)
    heatmap_opacity = foreground[:, :, 3]
    heatmap_opacity[:] = 64
    threshold_prob = min(thresh , heatmap.max() - 0.05)
    heatmap_opacity[heatmap < threshold_prob] = 0
    foreground_image = Image.fromarray(foreground)
    image = Image.alpha_composite(background_image, foreground_image)
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])
    image_array = np.array(background, dtype=np.uint8)
    return image_array


def zero_one_normalize(array):
    """Normalize array in 0 and 1.

    .. math :: I_{norm} = (I - I_{min}) / (I_{max} - I_{min})

    Arguments
    ---------
    array: ndarray
        Input array to be normalized.

    Returns
    -------
    ndarray
        Returns a normalized array. If min value and max value of array are
        equal, then returns the array.

    """
    if array.min() == array.max():
        if array.max() == 0:
            return array
        return array / array.max()
    array = array - array.min()
    array = array / array.max()
    return array


def conv_averaged(array, kernel_size=7):
    """Average using convolution.

    Runs a kernel of 1s of given size of the input array and each output pixel
    is divided by the total number of times convolution kernel was applied on
    the pixel on that location in input array.

    Arguments
    ---------
    array: ndarray
        A 2-d numpy array.
    kernel_size: int
        Kernel size of the convolution to be used, default is 7.

    Returns
    -------
    ndarray
        Conv averaged numpy array of same shape as input.

    """
    assert array.ndim == 2, \
        "Conv averaging can be applied only on 2d arrays."
    conv_kernel = np.ones((1, 1, kernel_size, kernel_size))
    ones_array = np.ones(array.shape)
    ones_array = ones_array[np.newaxis, np.newaxis, :]
    array = array[np.newaxis, np.newaxis, :]

    ones_array = Variable(torch.Tensor(ones_array).cuda())
    conv_kernel = Variable(torch.Tensor(conv_kernel).cuda())
    array = Variable(torch.Tensor(array).cuda())
    padding = int((kernel_size - 1) / 2)
    array = F.conv2d(array, conv_kernel, stride=1, padding=padding)
    ones_array = F.conv2d(ones_array, conv_kernel,
                          stride=1, padding=padding)
    return torch.div(array.data, ones_array.data).cpu().numpy()[0][0]