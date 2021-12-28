from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .templatetags import temp_tags

urlpatterns = [
    path("", views.MainPageView.as_view(), name="MainPage"),
    path("Login/", views.LoginView.as_view(), name="Login"),
    path("Register/", views.RegisterView.as_view(), name="Register"),
    path("UpdateInfo/", views.UpdateInfoView.as_view(), name="UpdateInfo"),
    path("ChangePassword/", views.ChangePass.as_view(), name="ChangePass"),
    path("DKCN/<str:TheLoaiCau>/", views.DangkyCauNguyen.as_view(), name="DKCN"),
    path("Update/<str:TheLoaiCau>/<int:id>/", views.UpdateCauNguyen.as_view(), name="Update"),
    path("Cung/<str:Phat>/", views.CungPhat.as_view(), name="CungPhat"),
    path("<str:Open>/<str:TheLoai>/", views.List.as_view(), name="List"),
    path("<str:Open>/<str:TheLoai>/<int:ID>/", views.Filter.as_view(), name="Filter"),
    path("<str:Open>/<str:TheLoai>/<str:Ten>/", views.Read.as_view(), name="Read"),
    path("LienHe/", views.LienHe.as_view(), name="LienHe"),
    path("Delete/", temp_tags.delete, name="Delete"),
    path("ChangePassword/", views.ChangePass.as_view(), name="ChangePass"),
    path("Logout", views.logout_view, name="Logout"),
    url(r'^Search/', include('haystack.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)