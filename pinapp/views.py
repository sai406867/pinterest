from django.shortcuts import render, get_object_or_404, redirect
from pinapp.models import Image, Comments, Category, Follow
from pinapp.forms import ImageUploadForm, CommentsForm
from django.http import HttpResponse
from datetime import datetime
#from .models import Board  
from .models import SavedImage



def base(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'base.html', context)

def category(request):
    categories = Category.objects.all()
    for i in categories:
        print(i.id)
    if request.GET.get('q'):
       query = request.GET.get('q')
       categories = Category.objects.filter(title__icontains=query)

    context = {'categories': categories}
    return render(request, 'category.html', context)

def image_list(request, image_id, slug):
    images = Image.objects.filter(category=image_id)
    print(images)
    return render(request, 'image_list.html', {'images': images})


def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    comments = image.comments.all()
    is_following = Follow.objects.filter(user=request.user, image=image, followed=True).exists()
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.image = image
            new_comment.user_name = request.user.username  # Assign logged-in user as the commenter
            new_comment.save()
            return redirect('pinapp:image_detail', image_id=image_id)
    else:
        form = CommentsForm()

    return render(request, 'image_detail.html', {'i': image, 'comments': comments, 'form': form,'is_following': is_following})
def like(request):
    return render(request, 'like.html')
    


def success(request):
    return render(request,'success.html')
def delete_image(request, pk):
    return render(request,'detail.html',context)

def download_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    print(image)

    response = HttpResponse(image.image, content_type='image')
    response['Content-Disposition'] = f'attachment; filename="{image.title}.png"'

    return response

def more_images(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    related_images = Image.objects.filter(category=image.category).exclude(pk=image_id)[:6]

    return render(request, 'more_images.html', {'image': image, 'related_images': related_images})
  


def index(request):
	
 return render(request,'index.html')
 from pinapp.models import Image, Follow

def follow_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    user = request.user
    follow_instance, created = Follow.objects.get_or_create(user=user, image=image)

    if 'follow' in request.POST:
        follow_instance.followed = True
    elif 'unfollow' in request.POST:
        follow_instance.followed = False
    
    follow_instance.save()
    return redirect('pinapp:image_detail', image_id=image_id)

def create_pin(request):
    c=Image.objects.all()
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')
        upload_date = request.POST.get('upload_date')
        slug = request.POST.get('slug')
        category = request.POST.get('category')  # Assuming you have a category_id field in the form

        # Create a new Image object and save it to the database
        new_image = Image(
            image_id=image_id,
            title=title,
            description=description,
            image=image_file,
            upload_date=upload_date,
            slug=slug,
            category=category  # Assign the category ID
        )
        new_image.save()
        # Redirect to a success page or any other appropriate page
        return redirect('success_page')  # Change 'success_page' to the URL name of your success page

    return render(request, 'create_pin.html',{'c':c})

from django.shortcuts import get_object_or_404
from .models import Image  # Import your Image model
from datetime import datetime

def create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            category_id = request.POST.get('category')
            
            # Instead of fetching Category object, save directly to Image model
            image_instance.title = title
            image_instance.description = description
            image_instance.image = request.FILES['image']
            image_instance.upload_date = datetime.now()
            image_instance.category_id = category_id  # Assign category ID directly

            image_instance.save()
            return redirect('pinapp:success')  # Redirect to a success URL after saving
    else:
        form = ImageUploadForm()

    return render(request, 'create.html', {'form': form, 'categories': categories})



#===========================================================================================
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def save_image(request, image_id):
    # Get the image object based on the image_id
    image = get_object_or_404(Image, pk=image_id)

    # Create a SavedImage object for the logged-in user and the image
    SavedImage.objects.get_or_create(user=request.user, image=image)

    # Return a success response
    return redirect('pinapp:display_saved_images')


@login_required
def display_saved_images(request):
    # Get all the saved images for the logged-in user
    saved_images = SavedImage.objects.filter(user=request.user)

    return render(request, 'saved_images.html', {'saved_images': saved_images})


def download_saved_image(request, image_id):
    # Retrieve the image object using the image_id
    image = get_object_or_404(YourImageModel, pk=image_id)  # Replace 'YourImageModel' with your actual model

    # Assuming the image is stored in a 'image_field' field within the model
    image_data = image.image_field.read()
    
    # Create an HTTP response with the image data as content
    response = HttpResponse(image_data, content_type='image')  # Modify content_type based on your image type

    # Set the appropriate content disposition for download
    response['Content-Disposition'] = f'attachment; filename="{image.filename}"'  # Provide the image filename

    return response
def explore(request):
    return render(request, 'explore.html')
    

    





