from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(models.Model):
    title = models.TextField(max_length=100)

    img = models.ImageField(upload_to='category/')
    

    slug = models.SlugField()
    def __str__(self):
        return self.title

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=100)
    description=models.TextField(max_length=10000)
    image = models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.title
        pass

class Comments( MPTTModel):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=50)
    comment = models.TextField(max_length=100) 
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
from django.contrib.auth.models import User

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    followed = models.BooleanField(default=False)
from django.contrib.auth.models import User
class SavedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    # You can include other fields as needed

    def __str__(self):
        return f"{self.user.username}'s saved image - {self.image.title}"

#============================================================================
from .models import Image

def download_image(request, pk):
    # Fetch the image object using the primary key (pk)
    image = get_object_or_404(Image, pk=pk)

    # Create an HTTP response containing the image data
    response = HttpResponse(image.image, content_type='image')
    response['Content-Disposition'] = f'attachment; filename="{image.title}.png"'

    return redirect('pinapp:base')
    