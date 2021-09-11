from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from .models import Delivery

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A5
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing 

today = datetime.today()


# Render PDF for Delivery
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

	barcode_info = """
		{0} \n
		Unidades: {1} \n
		Cliente: {2} \n
		Data: {3}
	""".format(delivery_obj.obj.description, delivery_obj.quantity, delivery_obj.seller.name, delivery_obj.date)

	qr_code = qr.QrCodeWidget(barcode_info)
	bounds = qr_code.getBounds()
	width = bounds[2] - bounds[0]
	height = bounds[3] - bounds[1]

	d = Drawing(60, 60, transform=[60./width,0,0,60./height,0,0])
	d.add(qr_code)
	d.drawOn(c, 23, 480)


	for line in lines:
		text.textLine(line)

	c.drawText(text)
	c.showPage()
	c.save()
	buf.seek(0)

	return FileResponse(buf, as_attachment=False, filename="registo_entrega-{0}.pdf".format(delivery_id))