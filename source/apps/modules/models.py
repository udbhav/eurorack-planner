import os, urllib, json, StringIO

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File  # you need this somewhere
from django.core.mail import EmailMessage

from PIL import Image

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

class Manufacturer(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    image = models.ImageField(blank=True,null=True,upload_to="modules/images/")
    medium_image = ImageSpecField([ResizeToFit(width=800, height=325),], image_field='image', format='JPEG', options={'quality': 90})
    hp = models.IntegerField("HP", blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    current_12v = models.IntegerField("+12v (mA)", blank=True, null=True)
    negative_current_12v = models.IntegerField("-12v (mA)", blank=True, null=True)
    current_5v = models.IntegerField("5v (mA)", blank=True, null=True)
    msrp = models.DecimalField("MSRP ($)", max_digits=8, decimal_places=2, blank=True, null=True)
    url = models.CharField(blank=True, max_length=200)
    user = models.ForeignKey(User, blank=True, null=True)
    custom = models.BooleanField(blank=True)
    eurorackdb_id = models.IntegerField(blank=True, null=True, db_index=True)
    eurorackdb_image = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    def autocomplete_name(self):
        return '%s %s' % (self.manufacturer.name, self.name)

    def get_eurorackdb_image_path(self):
        if self.eurorackdb_image:
            return 'http://eurorackdb.com/assets/%s' % self.eurorackdb_image        
        else:
            return None

    def get_display_image_url(self):
        if self.image:
            return self.medium_image.url
        elif self.eurorackdb_image:
            return self.get_eurorackdb_image_path()
        else:
            return ''

    def save_eurorackdb_image(self):
        image_path = self.get_eurorackdb_image_path()
        if image_path:
            result = urllib.urlretrieve(image_path) 
            if result:
                self.image.save(
                    os.path.basename(image_path),
                    File(open(result[0]))
                    )
                self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('module', [str(self.id)])

class Setup(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    preset = models.TextField()

    def __unicode__(self):
        return self.name

    def build_image(self):
