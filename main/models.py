from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import date
from ckeditor.fields import RichTextField


class Blog(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.SET_NULL, null=True)
    #description = models.TextField(help_text='Write your blog')
    description = RichTextField()
    mini_description = models.TextField()
    post_date = models.DateField(default=date.today)
    slug = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.author}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + '-' + str(self.post_date))
        return super().save()


class BlogComment(models.Model):
    description = models.TextField(help_text='Write your comment')
    author = models.ForeignKey(User, related_name='blogcomments', on_delete=models.SET_NULL, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, related_name='blogcomments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.blog}, commented by {self.author}"


class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    phone_number = models.IntegerField()
    contact_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" 