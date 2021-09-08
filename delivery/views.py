from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from .models import Delivery

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A5

today = datetime.today()


# Render PDF
def render_pdf(request, delivery_id):
	delivery_id = str(delivery_id)

	buf = io.BytesIO()
	c = canvas.Canvas(buf, pagesize=A5, bottomup=0)

	delivery_obj = Delivery.objects.get(pk=delivery_id)
	lines = []

	c.setTitle("Registo de Entrega de Jornais (" + delivery_obj.seller.name + " - " + str(delivery_obj.date) + ")")
	text = c.beginText()
	text.setTextOrigin(cm, cm)
	text.setFont("Helvetica", 11)

	# for delivery in all_deliveries:
	# Header
	lines.append("RIO MAIOR JORNAL")
	lines.append("Registo de Entrega de Jornais")

	lines.append("")
	lines.append("")
	lines.append("- VENDEDOR -")
	lines.append("")
	
	lines.append("Vendedor: " + delivery_obj.seller.name)

	if delivery_obj.seller.phone is not None:
		lines.append("Telefone: " + delivery_obj.seller.phone)

	lines.append("Morada: " + delivery_obj.seller.address)

	lines.append("")
	lines.append("- OBJETO -")
	lines.append("")

	lines.append("Objeto Entregue: " + delivery_obj.obj.description)
	lines.append("Quantidade Entregue: " + str(delivery_obj.quantity))
	lines.append("Data da Entrega: " + str(delivery_obj.date))

	lines.append("")

	lines.append("Valor por Unidade (público): " + str(delivery_obj.obj.unit_price) + " €")
	lines.append("Valor por Unidade (vendedor): " + str(delivery_obj.obj.seller_revenue) + " €")

	lines.append("")
	lines.append("- RECOLHA DE SOBRAS -")
	lines.append("")

	lines.append("Data da Recolha: " + str(delivery_obj.date + timedelta(days=14)))

	lines.append("")
	lines.append("")
	lines.append("")

	lines.append("Confirmo que recebi {0} unidade(s) do {1}.".format(str(delivery_obj.quantity), delivery_obj.obj.description))
	lines.append("")
	lines.append("")
	lines.append("_____________________")
	
	lines.append("")
	lines.append("")
	lines.append("")
	lines.append("")
	lines.append("ID Entrega: " + str(today.year) + "-" + str(delivery_id))


	for line in lines:
		text.textLine(line)

	c.drawText(text)
	c.showPage()
	c.save()
	buf.seek(0)

	return FileResponse(buf, as_attachment=False, filename="registo_entrega-{0}.pdf".format(delivery_id))