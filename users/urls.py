from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name="edit-account"),

    path('apply/', views.applyIntern, name="apply"),
    path('review/', views.reviewInterns, name="review"), 

    path('accept_intern/<str:intern_id>', views.acceptIntern, name="accept_intern"),
    path('reject_intern/<str:intern_id>', views.rejectIntern, name="reject_intern"),

    path('interns/', views.displayInterns, name="interns"),
    path('user-profile/<str:id>/', views.singleUserPage, name="user-profile"),

    path('create-users/', views.createUsers, name = "create-users"),

    path('export/', views.export_to_excel, name='export_to_excel'),

]