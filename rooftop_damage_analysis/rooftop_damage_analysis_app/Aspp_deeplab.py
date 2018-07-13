import torch.nn as nn
import torch


class Aspp(nn.Module):

    def __init__(self, num_classes):
        super(Aspp, self).__init__()
        self.conv1X1 = nn.Conv2d(512, 512, kernel_size=1)
        self.bn1 = nn.BatchNorm2d(512)

        self.conv3X3 = nn.Conv2d(512, 512, kernel_size=3, dilation=6,
                                 padding=6)
        self.bn2 = nn.BatchNorm2d(512)
        self.dropout1 = nn.Dropout(0.5)

        self.conv3X3_2 = nn.Conv2d(512, 512, kernel_size=3, dilation=12,
                                   padding=12)
        self.bn3 = nn.BatchNorm2d(512)

        self.dropout2 = nn.Dropout(0.5)

        self.conv3X3_3 = nn.Conv2d(512, 512, kernel_size=3, dilation=18,
                                   padding=18)
        self.bn4 = nn.BatchNorm2d(512)

        self.dropout3 = nn.Dropout(0.5)

        self.imgpool = nn.AvgPool2d(8)

        self.bilinear = nn.UpsamplingBilinear2d(scale_factor=8)

        self.conv1x1_final = nn.Conv2d(2560, 256, kernel_size=1)
        self.bn5 = nn.BatchNorm2d(256)

        self.conv1x1_last = nn.Conv2d(256, num_classes, kernel_size=1)
        self.bilinear_2 = nn.UpsamplingBilinear2d(scale_factor=8)

    def forward(self, x):
        a = self.conv1X1(x)
        a = self.bn1(a)
        b = self.conv3X3(x)
        b = self.dropout1(self.bn2(b))
        c = self.conv3X3_2(x)
        c = self.dropout2(self.bn3(c))
        d = self.conv3X3_3(x)
        d = self.dropout3(self.bn4(d))

        e = self.imgpool(x)
        e = self.bilinear(e)

        x = torch.cat([a, b, c, d, e], 1)

        x = self.conv1x1_final(x)
        x = self.bn5(x)
        x = self.conv1x1_last(x)
        x = self.bilinear_2(x)

        return x
