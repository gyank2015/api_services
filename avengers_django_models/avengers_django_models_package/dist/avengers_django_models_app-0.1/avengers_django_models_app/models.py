from django.db import models
from django.utils import timezone
import jsonfield
# Create your models here.


choices = (
    (0, 'Submitted'),
    (1, 'Inqueue'),
    (2, 'Complete'),
    (3, 'Errored'),
)


class uploadedImages(models.Model):
    imageHash = models.CharField(max_length=32, default='default')  # md5 hash
    imageType = models.CharField(max_length=15, default='image/jpg')
    uploadedBy = models.CharField(max_length=100, default='default')  # Should be changees to auth-token once auth is implemented
    uploadedAt = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'uploaded_images'


class resultTable(models.Model):
    txnID_fileHash = models.CharField(max_length=50 + 32)
    submitTS = models.DateTimeField(default=timezone.now, null=True, blank=True)
    completeTS = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=choices)
    result = jsonfield.JSONField()

    class Mera:
        db_table = 'infer_result'
