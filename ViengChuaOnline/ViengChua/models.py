from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import ExtractYear
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now


class CommonInfo(models.Model):
    HoTen = models.CharField("Họ và Tên", max_length=50)
    NgaySinh = models.DateField("Ngày Sinh", default=timezone.now)
    PhapDanh = models.CharField("Pháp Danh", max_length=50, null=True, blank=True)
    GioiTinh_Choices = (
        ("Nam", "Nam"),
        ("Nữ", "Nữ"),
    )
    GioiTinh = models.CharField("Giới Tính", max_length=3, choices=GioiTinh_Choices)
    DiaChi = models.CharField("Địa Chỉ", max_length=60)
    QueQuan = models.CharField("Quê Quán", max_length=60)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.HoTen


class MyUser(AbstractUser, CommonInfo):

    class Meta:
        ordering = ("date_joined", "username", )

    def __str__(self):
        return self.username

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in MyUser._meta.fields]


class InfoCauNguyen(models.Model):
    Image = models.ImageField("Hình Ảnh", upload_to="CauNguyen")
    LoiCauNguyen = models.TextField("Lời Cầu Nguyện")
    ThoiGianCauNguyen = models.DateTimeField("Thời Gian", default=now)
    CommentUser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    
    class Meta:
        abstract: True


class InfoCauAn(CommonInfo, InfoCauNguyen):

    class Meta:
        ordering = ("-ThoiGianCauNguyen", )

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in InfoCauAn._meta.fields]

    def get_absolute_url(self):
        return reverse('Filter', kwargs={'Open': "List", 'TheLoai': "CauAn", 'ID': self.id})


class InfoCauSieu(CommonInfo, InfoCauNguyen):
    NgayMat = models.DateField("Ngày Mất")
    HuongDuong = models.PositiveIntegerField("Hưởng Dương")

    class Meta:
        ordering = ("-ThoiGianCauNguyen", )
        
    def get_absolute_url(self):
        return reverse('Filter', kwargs={'Open': "List", 'TheLoai': "CauSieu", 'ID': self.id})

    def save(self, *args, **kwargs):
        self.HuongDuong = ExtractYear(self.NgayMat) - ExtractYear(self.NgaySinh) + 1
        super(InfoCauSieu, self).save(*args, **kwargs)

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in InfoCauSieu._meta.fields]


class Book(models.Model):
    Name = models.CharField("Tên", max_length=150)
    TacGia = models.CharField("Tác giả", max_length=40)
    Upload = models.FileField(upload_to="Book")
    TheLoai_Choices = (
        ("LichSu", "Lịch sử"),
        ("NghiLe", "Nghi lễ"),
        ("PhatHoc", "Phật học"),
    )
    TheLoai = models.CharField("Thể Loại", max_length=30, choices=TheLoai_Choices)

    class Meta:
        ordering = ("Name", )
        
    def get_absolute_url(self):
        return reverse('Read', kwargs={'Open': "Book", 'TheLoai': self.TheLoai, 'Ten': self.Name})


class VanHoa(models.Model):
    Name = models.CharField("Tên", max_length=150)
    TacGia = models.CharField("Tác giả", max_length=40, null=True)
    Upload = models.FileField(upload_to="VanHoa")
    TheLoai_Choices = (
        ("SongDep", "Sống đẹp"),
        ("NauChay", "Nấu chay"),
        ("AnChay", "Ăn chay"),
    )
    TheLoai = models.CharField("Thể Loại", max_length=30, choices=TheLoai_Choices)

    class Meta:
        ordering = ("Name", )
        
    def get_absolute_url(self):
        return reverse('Read', kwargs={'Open': "VanHoa", 'TheLoai': self.TheLoai, 'Ten': self.Name})


class QuaLuuNiem(models.Model):
    Name = models.CharField("Tên", max_length=200, unique=True)
    Image = models.ImageField("Hình Ảnh", upload_to="Qua")
    Price = models.IntegerField("Giá", null=True)
    Description = models.TextField("Mô tả", max_length=10000, default="Chưa có mô tả")

    class Meta:
        ordering = ("Name", "Price", )

    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in QuaLuuNiem._meta.fields]
    
    def get_absolute_url(self):
        return reverse('Filter', kwargs={'Open': "List", 'TheLoai': "Qua", 'ID': self.id})


class InfoLienHe(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=254)
    Comment = models.TextField("Comment")
    Time = models.DateTimeField("Time", default=now)
    CommentUser = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ("Name", "Email", "Time", )

    def __str__(self):
        return self.Name
