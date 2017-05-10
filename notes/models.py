from colorful.fields import RGBColorField
from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    note_title = models.CharField(max_length=200)
    note_text = models.TextField(max_length=10000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    labels = models.ManyToManyField('Label', related_name='notes')
    public = models.BooleanField(default=0)
    archived = models.BooleanField(default=0)

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.timestamp <= now

    # def get_absolute_url(self):
    #     return reverse("notes:detail", kwargs={"slug": self.slug})
    #     # return reverse('notes:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.note_title

    class Meta:
        ordering = ["-timestamp", "-updated"]


# def create_slug(text, new_slug=None):
#     slug = slugify(text)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Note.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug(text, new_slug=new_slug)
#     return slug
#
#
# #
# # def get_image_filename(filename):
# #     slug = create_slug(filename)
# #     return "post_images/%s" % slug
#
#
# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance.note_title)
#
#
# pre_save.connect(pre_save_post_receiver, sender=Note)


class Label(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, default="")
    background_color = RGBColorField(default="#ffffff")
    text_color = RGBColorField(default="#000000")

    def __str__(self):
        return self.text
