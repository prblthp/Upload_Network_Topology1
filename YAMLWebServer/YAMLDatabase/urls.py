from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header = "Network Database"
admin.site.site_title = "Welcome to admin Dashboard"
admin.site.index_title = "Welcome to this portal!"

urlpatterns = [
    path('admin/',admin.site.urls),
    path('dashboard/<int:note_id>/',views.yamldisplays, name = "yamldisplays"),
    path('filedisplay/',views.filenamedisplay, name = "filenamedisplay"),
    path('<filename_id>/',views.index, name="index"),
    path('deletefile/<int:id>', views.filenamedelete, name = "filenamedelete"),
    path('',views.filenameinsert, name="filenameinsert"),
    path('edit/<int:id>',views.yamledit,name = "yamledit"),
    path('update/<int:id>', views.yamlupdate, name = "yamlupdate"),
    path('delete/<int:id>', views.yamldelete1, name = "yamldelete1")

]
