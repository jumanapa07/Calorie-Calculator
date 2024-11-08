from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_view/", views.register_view, name="register_view"),

    path("register/", views.register),
    path("loginn/", views.loginn,name="login"),
    path("user_logout/", views.user_logout,name="logout"),
    path("profile/", views.profile,name="profile"),
    path("editprofile/", views.editprofile,name="editprofile"),



    path("home/", views.home,name="home"),
    path("dayLog/", views.dayLog,name="dayLog"),
    path("view_logs/", views.view_logs,name="view_logs"),

    path("add_meal/", views.add_meal,name="add_meal"),
    path("deletefood/", views.deletefood,name="deletefood"),
    path("editfood/", views.editfood,name="editfood"),

    path("add_exercise/", views.add_exercise,name="add_exercise"),
    path("deleteexercise/", views.deleteexercise,name="deleteexercise"),
    path("editexercise/", views.editexercise,name="editexercise"),

    path("deleteweight/", views.deleteweight,name="deleteweight"),
    path("editweight/", views.editweight,name="deletefood"),

    path("plan/", views.plan,name="plan"),
    path("search/", views.search,name="search"),

    path("goal/", views.goal,name="goal"),
    path("progress/", views.progress,name="progress"),

    path("food/", views.food_list_view,name="food"),
    path('food/<str:food_id>', views.food_details_view, name='food_details'),


    # path("weight/",views.weight,name="weight"),









]