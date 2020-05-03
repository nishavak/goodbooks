from django.contrib import admin
from .models import Author, Book, Feedback, Profile, Tag


admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Feedback)
admin.site.register(Profile)
admin.site.register(Tag)
