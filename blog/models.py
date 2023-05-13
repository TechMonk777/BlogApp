from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.
class Tag(models.Model):
    caption     = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.caption}"
class Author(models.Model):
    first_name  = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    email       = models.EmailField() 
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
class Post(models.Model):
    title       = models.CharField(max_length=100)
    excert      = models.CharField(max_length=100)
    img_name    = models.ImageField(upload_to="posts",null=True)
    date        = models.DateField(auto_now=True)
    content     = models.TextField(validators=[MinLengthValidator(10)])
    author      = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    tags        = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"{self.title}"
    
class Comments(models.Model):
    user_name = models.CharField(max_length=40)
    user_email = models.EmailField()
    text = models.TextField(max_length=200)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

    def __str__(self) -> str:
        return f"{self.user_name}'s comment"
    