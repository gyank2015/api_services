from djongo import models
from django.utils import timezone
import jsonfield
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.


class customListField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(customListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value:
            return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([str(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

choices = (
    (0, 'Submitted'),
    (1, 'Inqueue'),
    (2, 'Complete'),
    (3, 'Errored'),
)

infer_requests_status_choices = (
    (0, 'Submitted'),
    (1, 'Processing'),
    (2, 'Complete'),
    (3, 'Errored'),
)


class uploadedImages(models.Model):
    imageHash = models.CharField(max_length=32, default='default')  # md5 hash
    imageType = models.CharField(max_length=15, default='jpg')
    uploadedBy = models.CharField(max_length=100, default='default')  # Should be changees to auth-token once auth is implemented
    uploadedAt = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'uploaded_images'


class resultTable(models.Model):
    txnID_fileHash = models.CharField(max_length=50 + 32)
    submitTS = models.DateTimeField(default=timezone.now, null=True, blank=True)
    completeTS = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=choices, default=0)
    result = jsonfield.JSONField()

    class Meta:
        db_table = 'infer_result'


class inferRequests(models.Model):
    txnID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fileHashes = customListField()
    DLmodel = models.CharField(default='not_chosen', max_length=100)
    authToken = models.CharField(default='not yet implemented', max_length=100)
    status = models.IntegerField(choices=infer_requests_status_choices, default=0)
    nos_hashes_submitted = models.IntegerField(default=0)
    nos_hashes_inferred = models.IntegerField(default=0)

    class Meta:
        db_table = 'infer_requests'



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()



