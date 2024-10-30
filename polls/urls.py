from django.urls import path
from . import views
from .views import BBLoginView 
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('account/login', BBLoginView.as_view(), name='login'),
    
]