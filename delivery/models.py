from django.db import models


class Seller(models.Model):
	name = models.CharField('Nome', max_length=255)
	address = models.TextField('Morada/Localidade', max_length=255)
	phone = models.CharField('Telefone/Telemóvel', max_length=9, blank=True, null=True)
	nif = models.CharField('NIF', max_length=9, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Vendedor'
		verbose_name_plural = 'Vendedores'


class Object(models.Model):
	description = models.CharField('Descrição', max_length=255)
	unit_price = models.DecimalField('Valor Unitário (venda)', max_digits=3, decimal_places=2)
	seller_revenue = models.DecimalField('Valor Unitário (vendedor)', max_digits=3, decimal_places=2)

	def __str__(self):
		return self.description

	class Meta:
		verbose_name = 'Publicação'
		verbose_name_plural = 'Publicações'


class Delivery(models.Model):
	date = models.DateField('Data')
	seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
	obj = models.ForeignKey(Object, on_delete=models.CASCADE)
	quantity = models.IntegerField('Quantidade')
	notes = models.TextField('Notas', blank=True, null=True)

	def __str__(self):
		return "{0} - {1}".format(self.seller, self.obj)

	class Meta:
		verbose_name = 'Entrega'
		verbose_name_plural = 'Entregas'


class Leftovers(models.Model):
	pickup_date = models.DateField('Data de Recolha', blank=True)
	quantity = models.IntegerField('Quantidade', blank=True)
	delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, blank=True, null=True)
	obj = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return "Sobras de {0} ({1})".format(self.delivery.seller.name, self.delivery.obj.description)

	class Meta:
		verbose_name = 'Sobra'
		verbose_name_plural = 'Sobras'