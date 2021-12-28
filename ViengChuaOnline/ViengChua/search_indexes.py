from haystack import indexes
from .models import InfoCauAn, InfoCauSieu, Book, VanHoa
	
	
class CauAnIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.EdgeNgramField(document=True, use_template=True)
	content_auto1 = indexes.EdgeNgramField(model_attr="HoTen")
	content_auto2 = indexes.EdgeNgramField(model_attr="NgaySinh")
	content_auto3 = indexes.EdgeNgramField(model_attr="PhapDanh", null=True)
	content_auto4 = indexes.EdgeNgramField(model_attr="GioiTinh")
	content_auto5 = indexes.EdgeNgramField(model_attr="DiaChi")
	content_auto6 = indexes.EdgeNgramField(model_attr="QueQuan")
	content_auto7 = indexes.EdgeNgramField(model_attr="CommentUser")
	content_auto8 = indexes.EdgeNgramField(model_attr="LoiCauNguyen")
	
	def get_model(self):
		return InfoCauAn
	
	def index_queryset(self, using=None):
		return self.get_model().objects.all()


class CauSieuIndex(CauAnIndex):
	content_auto9 = indexes.EdgeNgramField(model_attr="NgayMat")
	content_auto10 = indexes.EdgeNgramField(model_attr="HuongDuong")
	
	def get_model(self):
		return InfoCauSieu
	
	
class BookIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.EdgeNgramField(document=True, use_template=True)
	content_auto1 = indexes.EdgeNgramField(model_attr="Name")
	content_auto2 = indexes.EdgeNgramField(model_attr="TacGia")
	content_auto3 = indexes.EdgeNgramField(model_attr="TheLoai")
	
	def get_model(self):
		return Book
	
	
class VanHoaIndex(BookIndex):
	text = indexes.CharField(document=True, use_template=True)

	def get_model(self):
		return VanHoa