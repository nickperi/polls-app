from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name = "polls"
urlpatterns = [
    path('/<int:user_id>', views.index_view, name="index"),
    path('profile/voter<int:user_id>', views.profile_view, name="profile"),
    path('login-user', views.login_user, name="login"),
    path('logout-user', views.logout_user, name="logout"),
    path('vote/question<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('question<int:question_id>/voter<int:user_id>/results/', views.results_view, name="results"),
    path('question<int:question_id>/voter<int:user_id>/vote/', views.vote, name="vote"),
    path('choice-voters/choice<int:choice_id>/question<int:question_id>', views.choice_view, name="choice-voters")
]