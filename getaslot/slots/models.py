from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

# Create your models here.
class Business(models.Model):
    """
    A model for Business
    """
        
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200)
    owner = models.ForeignKey(User, related_name="businesses")
    description = models.TextField(_("body"))
    created_at = models.DateTimeField(_("created at"), default=datetime.now)
    picture = models.ImageField(_(u"Picture"),upload_to="business_pictures/", blank=True,null=True)    
    
    class Meta:
        verbose_name = _("business")
        verbose_name_plural = _("businesses")
        ordering = ["-created_at"]
        get_latest_by = "created_at"
    
    def __unicode__(self):
        return self.title
    
    def save(self, **kwargs):
        super(Business, self).save(**kwargs)
    
    def get_absolute_url(self):
        return reverse("business", kwargs={
            "slug": self.slug
        })
class BusinessEmployee(models.Model):
    business = models.ForeignKey(Business, related_name="employees")
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), blank=True, null=True)
    
    class Meta:
        ordering = ['business','name']
    def __unicode__(self):
        return self.name

class WorkSchedule(models.Model):
    employee = models.ForeignKey(BusinessEmployee, related_name="work_schedules")
    starttime = models.DateTimeField(_("start time"))
    endtime = models.DateTimeField(_("end time"))
    day = models.DateField(_("date"), blank=True, null=True)
    class Meta:
        ordering = ['-endtime']
    def __unicode__(self):
        return u"%s %s - %s" % (unicode(self.employee),
                      self.starttime.strftime(u'%Y-%m-%d %H:%M'),
                      self.endtime.strftime(u'%Y-%m-%d %H:%M'),
                      )
    def save(self, **kwargs):
        self.day = self.starttime.date()
        super(WorkSchedule, self).save(**kwargs)

class Appointment(models.Model):
    work_schedule = models.ForeignKey(WorkSchedule, related_name="appointments")
    starttime = models.DateTimeField(_("start time"))
    endtime = models.DateTimeField(_("end time"))
    day = models.DateField(_("date"), blank=True, null=True)
    customer = models.ForeignKey(User, related_name="appointments", blank=True, null=True)
    name = models.CharField(_("name"), max_length=200, blank=True, null=True)
    phone = models.CharField(_("phone"), max_length=200, blank=True, null=True)
    reminder_sent = models.BooleanField(_("reminder sent"), default=False)
    class Meta:
        ordering = ['-endtime']
    def __unicode__(self):
        return u"%s %s - %s" % (unicode(self.name),
                      self.starttime.strftime(u'%Y-%m-%d %H:%M'),
                      self.endtime.strftime(u'%Y-%m-%d %H:%M'),
                      )
    def save(self, **kwargs):
        self.day = self.starttime.date()
        super(WorkSchedule, self).save(**kwargs)
