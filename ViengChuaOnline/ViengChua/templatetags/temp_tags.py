from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.utils.safestring import SafeString

from ..models import InfoCauSieu, InfoCauAn, Book, VanHoa, QuaLuuNiem

register = template.Library()


@register.simple_tag(takes_context=True)
def get_User(context):
    request = context["request"]
    try:
        if request.session["user_id"] != "":
            return request.session["user_id"]
        else:
            return "Đăng Nhập"
    except:
        return "Đăng Nhập"


@register.simple_tag()
def Choose(Open, TheLoai):
    Display = ""
    if Open == "List":
        if TheLoai == "CauAn":
            Display = InfoCauAn.objects.all()
        if TheLoai == "CauSieu":
            Display = InfoCauSieu.objects.all()
        if TheLoai == "Qua":
            Display = QuaLuuNiem.objects.all()
        return Display
    if Open == "Book":
        return Book.objects.filter(TheLoai=TheLoai)
    else:
        if Open == "VanHoa":
            return VanHoa.objects.filter(TheLoai=TheLoai)
    return HuongDan.objects.all()


@register.simple_tag(takes_context=True)
def get_List(context, Open, TheLoai, ID):
    request = context["request"]
    u = context["request"].user
    Display = Choose(Open, TheLoai)
    if SafeString(ID) == SafeString(0):
        Display = Choose(Open, TheLoai).filter(CommentUser__username=u.username)
    if SafeString(ID) > SafeString(0):
        Display = Choose(Open, TheLoai).filter(id=ID)
        return Display
    HienThi = Paginator(Display, 3)
    page = request.GET.get('page')

    try:
        Paginated = HienThi.get_page(page)
    except PageNotAnInteger:
        Paginated = HienThi.get_page(1)
    except EmptyPage:
        Paginated = HienThi.get_page(HienThi.num_pages)
    return Paginated


@login_required
def delete(request):
    if request.is_ajax() and request.method == "POST":
        id = request.POST.get("id")
        TheLoai = request.POST.get("TheLoai")
        Open = request.POST.get("Open")
        try:
            Choose(Open, TheLoai).filter(id=id, CommentUser=request.user).delete()
            messages.success(request, "Đã xóa cầu nguyện")
        except:
            messages.error(request, "Xóa cầu nguyện lỗi/Bạn không có quyền xóa")
            return HttpResponse()
    return HttpResponse()

