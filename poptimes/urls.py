from django.urls import path
from . import views

app_name = 'poptimes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('<slug:category_id>/',
         views.CategoryView.as_view(), name='category'),
    path('<slug:company_id>/<slug:release_id>',
         views.EntryView.as_view(), name='detail'),
    # path('<slug:company_id>/<slug:release_id>/comment',
    #      views.send_comment, name='comment'),
]
