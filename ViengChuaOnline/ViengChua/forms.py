from django import forms
from django.forms import NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.utils.datetime_safe import date
from .models import MyUser, InfoCauAn, InfoCauSieu, InfoLienHe



class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username", "email", "password1", "password2")


class FullInfoForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ("username", "email", "HoTen", "NgaySinh", "PhapDanh", "GioiTinh", "DiaChi", "QueQuan")
        widgets = {
            "NgaySinh": NumberInput(attrs={"type": "date", "class": "ngay", "id": "ngaysinh"}),
        }

    def __init__(self, *args, **kwargs):
        super(FullInfoForm, self).__init__(*args, **kwargs)
        self.fields["username"].disabled = True
        self.fields["email"].disabled = True

    def clean(self):
        if date.today() < self.cleaned_data["NgaySinh"]:
            raise forms.ValidationError("*Please check the date")
        super(FullInfoForm, self).clean()


class CauAnForm(forms.ModelForm):
    class Meta:
        model = InfoCauAn
        exclude = ("CommentUser", "ThoiGianCauNguyen")
        widgets = {
            "NgaySinh": NumberInput(attrs={"type": "date", "class": "ngay", "id": "ngaysinh"}),
        }

    def form_save(self, form, username):
        self.object = form.save(commit=False)
        user = MyUser.objects.get(username=username)
        self.object.CommentUser = user
        self.object.save()
        
    def clean(self):
        if date.today() < self.cleaned_data["NgaySinh"]:
            raise forms.ValidationError("*Please check the date")
        super(CauAnForm, self).clean()


class CauSieuForm(forms.ModelForm):
    class Meta():
        model = InfoCauSieu
        exclude = ("CommentUser", "ThoiGianCauNguyen")
        widgets = {
            "NgaySinh": NumberInput(attrs={"type": "date", "class": "ngay", "id": "ngaysinh"}),
            "NgayMat": NumberInput(attrs={"type": "date", "class": "ngay", "id": "ngaymat"}),
        }

    def form_save(self, form, username):
        self.object = form.save(commit=False)
        user = MyUser.objects.get(username=username)
        self.object.CommentUser = user
        self.object.save()

    def clean(self):
        if self.cleaned_data["NgayMat"] < self.cleaned_data["NgaySinh"] \
                or date.today() < self.cleaned_data["NgaySinh"]\
                or date.today() < self.cleaned_data["NgayMat"]:
            raise forms.ValidationError("*Please check the date")
        super(CauSieuForm, self).clean()



class LienHeForm(forms.ModelForm):
    class Meta:
        model = InfoLienHe
        exclude = ("CommentUser", "Time", )

    def form_save(self, form, username):
        self.object = form.save(commit=False)
        user = MyUser.objects.get(username=username)
        self.object.CommentUser = user
        self.object.Name = user.username
        self.object.Email = user.email
        self.object.save()


