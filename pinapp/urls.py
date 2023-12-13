from django.urls import path
from pinapp.views import create_pin,category,image_list,base, delete_image, image_detail,download_image,more_images,follow_image,like,create,save_image,display_saved_images,download_image,success,explore
 

app_name='pinapp'
urlpatterns = [
    path('',category,name='category'),
    path('<int:image_id>/<slug:slug>/', image_list, name='image_list'),
    path('base/',base,name='base'),
    
    path('delete/<int:pk>/', delete_image, name='delete_image'),  # This line handles the delete_image view,
    path('image_detail/<int:image_id>/', image_detail, name='image_detail'),
    path('download/<int:pk>/', download_image, name='download_image'),
    path('like',like,name='like'),
    path('add_comment/<int:image_id>/', image_detail, name='add_comment'),
    path('create/', create, name='create'),
    path('follow_image/<int:image_id>/', follow_image, name='follow_image'),
    path('createpin/',create_pin,name="create_pin"),
    path('create_pin/', create_pin, name='create_pin'),
    path('save_image/<int:image_id>/', save_image, name='save_image'),
    path('saved_images/', display_saved_images, name='display_saved_images'),
    path('download/<int:pk>/', download_image, name='download_image'),
    path('success/', success, name='success'),
  
    path('explore/',explore,name='explore') 
      # Ensure the name is consistent here
    #path('board/',board, name='board'),

]


   

    

