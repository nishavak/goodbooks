from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


class Tag(models.Model):
    tagname = models.CharField(primary_key=True, max_length=50, default='')

    def __str__(self):
        return self.tagname


class Author(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=120)
    cover = models.ImageField(
        upload_to='covers/', null=True, blank=True, default='covers/none.jpg')
    tag = models.ManyToManyField(Tag)
    author = models.ManyToManyField(Author)
    quote = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    published_date = models.DateField()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, default='profile_pictures/default_pic.jpg')
    books = models.ManyToManyField(Book)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Feedback(models.Model):
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return str(self.rating)
