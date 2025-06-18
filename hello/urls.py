from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/user/<int:user_id>/", views.admin_user_detail, name="admin_user_detail"),
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("log/", views.log_message, name="log"),
    path("comment/<int:post_id>/add/", views.add_comment, name="add_comment"),
    path("register/", views.register, name="register"),
    path("message/<int:message_id>/edit/", views.edit_message, name="edit_message"),
    path("care/", views.care, name="care"),
]

