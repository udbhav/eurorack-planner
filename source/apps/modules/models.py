from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

class Manufacturer(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class ModuleImageURLField(object):
    name = 'full_image_url'
    serialize = True
    rel = None

    def _get_val_from_obj(self, obj):
        try:
            return obj.image.url
        except ValueError:
            return ''

    def value_to_string(self, obj):
        try:
            return obj.image.url
        except ValueError:
            return ''


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

    def get_display_image_url(self):
        if self.eurorackdb_image:
            return 'http://eurorackdb.com/assets/%s' % self.eurorackdb_image
        elif self.image:
            return self.medium_image.url
        else:
            return ''

    @models.permalink
    def get_absolute_url(self):
        return ('module', [str(self.id)])

class Setup(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    preset = models.TextField()

    def __unicode__(self):
        return self.name
