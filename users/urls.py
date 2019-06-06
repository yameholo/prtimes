from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('signup/', views.MyUserCreateView.as_view(), name='signup'),
    path('signup/done/', views.MySignupDoneView.as_view(), name='signup_done'),
    path('signup/complete/<str:uidb64>/<str:token>/',
         views.activate, name='signup_complete'),
    path('<slug:screen_name>/update/',
         views.MyUserUpdateView.as_view(), name='update'),
    path('password_change/', views.MyPasswordChangeView.as_view(),
         name='password_change'),
    path('<slug:screen_name>/delete/',
         views.MyUserDeleteView.as_view(), name='del'),
    path('password_reset/', views.MyPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>',
         views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
