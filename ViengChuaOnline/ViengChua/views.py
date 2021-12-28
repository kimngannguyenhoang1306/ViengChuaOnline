from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import os
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views import View
from .forms import RegisterForm, CauAnForm, FullInfoForm, CauSieuForm, LienHeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyUser, InfoCauAn, InfoCauNguyen, InfoCauSieu
from django.contrib import messages



def csrf_failure(request, reason=""):
    message = {'message': 'Cookie đã bị lỗi'}
    return HttpResponseRedirect("/Login/")


class MainPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
                request.session["user_id"] = request.user.username
                return render(request, "ViengChua/MainPage.html")
        return render(request, "ViengChua/MainPage.html")

    def post(self, request):
        pass


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            request.session["user_id"] = request.user.username
            return HttpResponseRedirect("/")
        else:
            form = AuthenticationForm()
            return render(request, "ViengChua/Register.html", {"form": form, "lg_name": "đăng nhập"})


    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.get_user() is not None:
                login(request, form.get_user())
                request.session["user_id"] = request.user.username
                messages.success(request, "Đăng nhập thành công")
                return HttpResponsePermanentRedirect(request.META.get("HTTP_REFERER"))
        return render(request, "ViengChua/Register.html", {"form": form, "lg_name": "đăng nhập"})


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            request.session["user_id"] = request.user.username
            return HttpResponseRedirect("/")
        else:
            form = RegisterForm()
            return render(request, "ViengChua/Register.html", {"form": form, "lg_name": "đăng ký tài khoản"})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session["user_id"] = username
                login(request, user)
                messages.success(request, "Đăng ký tài khoản thành công")
                return HttpResponsePermanentRedirect("/UpdateInfo/")
        messages.error(request, "Đăng ký tài khoản thất bại")
        return render(request, "ViengChua/Register.html", {"form": form, "lg_name": "đăng ký tài khoản"})


class UpdateInfoView(LoginRequiredMixin, View):
    login_url = "/Login/"
    def get(self, request):
        form = FullInfoForm(instance=request.user)
        return render(request, "ViengChua/Register.html", {"form": form, "lg_name": "cập nhật thông tin"})

    def post(self, request):
        updateUser = MyUser.objects.get(username=request.user.username)
        form = FullInfoForm(instance=updateUser, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật tài khoản thành công")
            return HttpResponsePermanentRedirect(request.META.get("HTTP_REFERER"))
        messages.error(request, "Cập nhật tài khoản thất bại")
        return render(request, "ViengChua/Register.html", {"form": form, "lg_name": "cập nhật thông tin"})


class ChangePass(LoginRequiredMixin, View):
    login_url = "/Login/"
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, "ViengChua/Register.html", {"form": form, "lg_name": "thay đổi mật khẩu"})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Thay đổi mật khẩu thành công")
            return HttpResponsePermanentRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "Thay đổi mật khẩu thất bại")
            return render(request, "ViengChua/Register.html", {"form": form, "lg_name": "thay đổi mật khẩu"})


class DangkyCauNguyen(LoginRequiredMixin, View):
    login_url = "/Login/"
    def get(self, request, TheLoaiCau):
        request.session["user_id"] = request.user.username
        if TheLoaiCau == "CauAn":
            form = CauAnForm()
            lg_name = "đăng ký cầu an"
        else:
            form = CauSieuForm()
            lg_name = "đăng ký cầu siêu"
        return render(request, "ViengChua/Register.html", {"form": form, "lg_name": lg_name})

    def post(self, request, TheLoaiCau):
        if TheLoaiCau == "CauAn":
            form = CauAnForm(request.POST, request.FILES)
            lg_name = "đăng ký cầu an"
        else:
            form = CauSieuForm(request.POST, request.FILES)
            lg_name = "đăng ký cầu siêu"
        if form.is_valid():
            form.form_save(form, request.session["user_id"])
            messages.success(request, "Đăng ký thành công")
            return redirect("List", Open="List", TheLoai=TheLoaiCau)
        else:
            messages.error(request, "Đăng ký thất bại")
            return render(request, "ViengChua/Register.html", {"form": form, "lg_name": lg_name})


class UpdateCauNguyen(LoginRequiredMixin, View):
    login_url = "/Login/"
    def get(self, request, TheLoaiCau, id):
        request.session["user_id"] = request.user.username
        try:
            if TheLoaiCau == "CauAn":
                form = CauAnForm(instance=InfoCauAn.objects.get(id=id, CommentUser=request.user))
                lg_name = "đăng ký cầu an"
            else:
                form = CauSieuForm(instance=InfoCauSieu.objects.get(id=id, CommentUser=request.user))
                lg_name = "đăng ký cầu siêu"
            return render(request, "ViengChua/Register.html", {"form": form, "lg_name": lg_name})
        except:
            return HttpResponsePermanentRedirect(request.META.get("HTTP_REFERER"))

    def post(self, request, TheLoaiCau, id):
        try:
            if TheLoaiCau == "CauAn":
                form = CauAnForm(instance=InfoCauAn.objects.get(id=id), data=request.POST, files=request.FILES)
                lg_name = "đăng ký cầu an"
            else:
                form = CauSieuForm(instance=InfoCauSieu.objects.get(id=id), data=request.POST, files=request.FILES)
                lg_name = "đăng ký cầu siêu"
            if form.is_valid():
                form.form_save(form, request.session["user_id"])
                messages.success(request, "Cập nhật cầu nguyện thành công")
                return redirect("List", Open="List", TheLoai=TheLoaiCau)
            else:
                messages.error(request, "Cập nhật cầu nguyện thất bại")
                return render(request, "ViengChua/Register.html", {"form": form, "lg_name": lg_name})
        except:
            messages.error(request, "Cập nhật cầu nguyện thất bại/Bạn không có quyền")
            return HttpResponsePermanentRedirect(request.META.get("HTTP_REFERER"))


class CungPhat(View):
    def get(self, request, Phat):
        request.session["user_id"] = request.user.username
        if Phat == "QuanAmBoTat":
            return render(request, "ViengChua/Phat.html")
        else:
            return render(request, "ViengChua/Phat1.html")

    def post(self, request, Phat):
        pass


class List(View):
    def get(self, request, Open, TheLoai):
        if request.user.is_authenticated:
                request.session["user_id"] = request.user.username
        return render(request, "ViengChua/List.html", {"TheLoai": TheLoai, "Open": Open})


class Filter(View):
    def get(self, request, Open, TheLoai, ID):
        if request.user.is_authenticated:
                request.session["user_id"] = request.user.username
        return render(request, "ViengChua/List.html", {"TheLoai": TheLoai, "Open": Open, "ID": ID})
    
    
class Read(View):
    def get(self, request, Open, TheLoai, Ten):
        if request.user.is_authenticated:
                request.session["user_id"] = request.user.username
        Ten = Ten.replace(" ", "_") + ".txt"
        file_path = os.path.join(settings.MEDIA_ROOT, Open, Ten)
        read = open(file_path, encoding="utf8").read().replace("\n", "")
        ChiaDoan = read.split("PhanTrang")
        HienThi = Paginator(ChiaDoan, 1)

        page = request.GET.get('page')

        try:
            Paginated = HienThi.get_page(page)
        except PageNotAnInteger:
            Paginated = HienThi.get_page(1)
        except EmptyPage:
            Paginated = HienThi.get_page(HienThi.num_pages)

        context = {
            "Paginated": Paginated,
            "TheLoai": TheLoai,
            "Open": Open,
        }
        return render(request, "ViengChua/Read.html", context)


class LienHe(View):
    def get(self, request):
        if request.user.is_authenticated:
            request.session["user_id"] = request.user.username
            form = LienHeForm(initial={"CommentUser": request.user.pk, "Name": request.user.HoTen, "Email": request.user.email},)
        else:
            form = LienHeForm()
        return render(request, "ViengChua/LienHe.html", {"form": form})

    def post(self, request):
        form = LienHeForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                form.form_save(form, request.session["user_id"])
            else:
                form.save()
                messages.success(request, "Đã gửi thông tin")
            return HttpResponsePermanentRedirect(request.META.get("HTTP_REFERER"))
        messages.error(request, "Thông tin chưa được gửi")
        return render(request, "ViengChua/Register.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Đã đăng xuất")
    return HttpResponsePermanentRedirect(request.META.get("HTTP_REFERER"))

