import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Note(models.Model):
    note_title = models.CharField(max_length=200)
    note_text = models.TextField(max_length=1000)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    labels = models.ManyToManyField('Label', related_name='notes')
    public = models.BooleanField(default=0)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_absolute_url(self):
        return reverse("notes:detail", kwargs={"slug": self.slug})
        # return reverse('notes:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.note_title

    class Meta:
        ordering = ["-timestamp", "-updated"]


def create_slug(text, new_slug=None):
    slug = slugify(text)
    if new_slug is not None:
        slug = new_slug
    qs = Note.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(text, new_slug=new_slug)
    return slug


def get_image_filename(filename):
    slug = create_slug(filename)
    return "post_images/%s" % slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance.note_title)


pre_save.connect(pre_save_post_receiver, sender=Note)


class Images(models.Model):
    note = models.ForeignKey(Note, default=None)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image', )


class Label(models.Model):
    text = models.CharField(max_length=200, default="")
    background_color = models.CharField(max_length=7, default="#ffffff")
    text_color = models.CharField(max_length=6, default="000000")

    def __str__(self):
        return self.text
