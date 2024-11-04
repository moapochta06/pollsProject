from django.urls import path
from . import views
from .views import user_activate
from .views import BBLoginView 
from .views import ChangeUserInfoView
from .views import BBLogoutView 
from .views import DeleteUserView
from .views import RegisterDoneView, RegisterUserView
from .views import profile
app_name = 'polls'
urlpatterns = [
    path('', views.base, name='base'),
    path('quest/', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/login', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/delete/', DeleteUserView.as_view(),name='profile_delete'),
]