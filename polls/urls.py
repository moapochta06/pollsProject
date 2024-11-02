from django.urls import path
from . import views
from .views import BBLoginView 
# from .views import change_user_info
from .views import ChangeUserInfoView
from .views import BBLogoutView 
from .views import DeleteUserView
from .views import profile
app_name = 'polls'
urlpatterns = [
    path('', views.base, name='base'),
    path('quest/', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('accounts/login', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    # path('accounts/profile/change/',change_user_info, name='profile_change'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/delete/', DeleteUserView.as_view(),name='profile_delete'),
]