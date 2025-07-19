from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name = "polls"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('<int:pk>/results/', views.ResultsView.as_view(), name="results"),
    path('<int:question_id>/<int:user_id>/vote/', views.vote, name="vote")
]