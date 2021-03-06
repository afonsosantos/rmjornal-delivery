from django.contrib import admin
from .models import Seller, Object, Delivery, Leftovers


admin.site.site_header = 'Rio Maior Jornal'
admin.site.site_title = 'Rio Maior Jornal'
admin.site.index_title = 'Aplicação de Gestão de Distribuição de Publicações'


class LeftoversInline(admin.TabularInline):
	model = Leftovers
	max_num = 1
	readonly_fields = ['total_vendidos']

	def total_vendidos(self, obj):
		if obj.quantity is None:
			return ''
		else:
			return obj.delivery.quantity - obj.quantity

@admin.register(Leftovers)
class LeftoversAdmin(admin.ModelAdmin):
	pass


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
	list_display = ['name', 'address', 'phone']


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
	list_display = ['description', 'unit_price', 'seller_revenue']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	list_display = ['id', 'date', 'seller', 'obj', 'quantity']
	readonly_fields = ['seller_revenue_total']
	actions = ['delivery_report']
	inlines = [LeftoversInline]
	list_filter = ('date', 'seller', 'obj')

	def seller_revenue_total(self, obj):
		return "{0} €".format(obj.obj.seller_revenue * obj.quantity)

	from .utils import delivery_report
	delivery_report.short_description = 'Imprimir Registo de Entrega'


class CustomAdminSite(admin.AdminSite):
	index_template = 'templates/admin/index.html'