from django.db import models
from django.conf import settings

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
    manufacturer = models.ForeignKey(Manufacturer)
    image = models.ImageField(blank=True,null=True,upload_to="modules/images/")
    hp = models.IntegerField(blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    current_12v = models.IntegerField(blank=True, null=True)
    negative_current_12v = models.IntegerField(blank=True, null=True)
    current_5v = models.IntegerField(blank=True, null=True)
    msrp = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    url = models.CharField(blank=True, max_length=200)

    def __unicode__(self):
        return self.name

    def autocomplete_name(self):
        return '%s %s' % (self.manufacturer.name, self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('module', [str(self.id)])

