from django.contrib import admin
from .models import MyUser, InfoCauAn, InfoCauSieu, Book, VanHoa, QuaLuuNiem, InfoLienHe
# Register your models here.


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
	list_display = ("username", "HoTen", "PhapDanh",)
	search_fields = ("username", "HoTen", "PhapDanh",)
	list_filter = ("GioiTinh",)
	
	
@admin.register(InfoCauAn)
class InfoCauAnAdmin(admin.ModelAdmin):
	list_display = ("HoTen", "PhapDanh", "ThoiGianCauNguyen", "CommentUser",)
	search_fields = ("HoTen", "PhapDanh", "CommentUser__username",)
	list_filter = ("GioiTinh",)
	readonly_fields = ("CommentUser", )

	
@admin.register(InfoCauSieu)
class InfoCauSieuAdmin(admin.ModelAdmin):
	list_display = ("HoTen", "PhapDanh", "ThoiGianCauNguyen", "CommentUser",)
	search_fields = ("HoTen", "PhapDanh", "CommentUser__username",)
	list_filter = ("GioiTinh",)
	readonly_fields = ("CommentUser", )


@admin.register(Book)
class Book(admin.ModelAdmin):
	list_display = ("Name", "TacGia", "TheLoai", )


@admin.register(VanHoa)
class VanHoa(admin.ModelAdmin):
	list_display = ("Name", "TacGia", "TheLoai", )


@admin.register(QuaLuuNiem)
class QuaLuuNiem(admin.ModelAdmin):
	list_display = ("Name", "Price", "Description", )


@admin.register(InfoLienHe)
class InfoLienHe(admin.ModelAdmin):
	list_display = ("Name", "Email")
	search_fields = ("Name", "Email", "CommentUser__username",)
	readonly_fields = ("CommentUser", )
