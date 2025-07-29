from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name = "polls"
urlpatterns = [
    path('/<int:user_id>', views.index_view, name="index"),
    path('profile/<int:user_id>', views.profile_view, name="profile"),
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('<int:question_id>/<int:user_id>/results/', views.results_view, name="results"),
    path('<int:question_id>/<int:user_id>/vote/', views.vote, name="vote"),
    path('choice/<int:choice_id>/', views.choice_view, name="choice")
]