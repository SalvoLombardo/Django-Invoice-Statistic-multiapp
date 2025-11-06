# crochet/models.py
from django.db import models


class CrochetPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="crochet_photos/")
    created_at = models.DateTimeField(auto_now_add=True)

    #FK
    author = models.ForeignKey("users.Client", on_delete=models.CASCADE, related_name="crochet_posts")


    def __str__(self):
        return self.title


class CrochetComment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    


    #FK
    author = models.ForeignKey("users.Client", on_delete=models.CASCADE)
    post = models.ForeignKey(CrochetPost, on_delete=models.CASCADE, related_name="comments")


    def __str__(self):
        return f"Comment by {self.author} on {self.post}"