import torch.nn as nn

from torchvision import models
from .Aspp_deeplab import Aspp


class DeeplabV3(nn.Module):

    def __init__(self, num_classes):
        super(DeeplabV3, self).__init__()

        self.resnet = modified_resnet()
        self.aspp = Aspp(num_classes)

    def forward(self, x):
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = self.resnet.relu(x)
        x = self.resnet.maxpool(x)
        x = self.resnet.layer1(x)
        x = self.resnet.layer2(x)
        x = self.resnet.layer3(x)
        x = self.resnet.layer4(x)
        x = self.aspp(x)

        return x


def modified_resnet():
    resnet = models.resnet18(pretrained=True)

    for module in resnet.layer3.modules():
        if isinstance(module, nn.Conv2d):
            if (module.stride == (2, 2)):
                module.stride = (1, 1)
            elif (module.kernel_size == (3, 3)):
                module.padding = (2, 2)
                module.dilation = (2, 2)

    for module in resnet.layer4.modules():
        if isinstance(module, nn.Conv2d):
            if (module.stride == (2, 2)):
                module.stride = (1, 1)
            elif (module.kernel_size == (3, 3)):
                module.padding = (4, 4)
                module.dilation = (4, 4)
    resnet._modules.popitem('fc')
    resnet._modules.popitem('avgpool')

    return resnet
