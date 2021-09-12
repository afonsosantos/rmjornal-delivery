import io
from datetime import datetime, timedelta

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.views.generic import TemplateView

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A5
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from chartjs.views.lines import BaseLineChartView

from .models import Delivery

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
	lines.append("Quantidade Recolhida: ___________")

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


class TotalMonthlyDeliveries(BaseLineChartView):
    def get_labels(self):
        return [
        	"Janeiro",
        	"Fevereiro",
        	"Março",
        	"Abril",
        	"Maio",
        	"Junho",
        	"Julho",
        	"Agosto",
        	"Setembro",
        	"Outubro",
        	"Novembro",
        	"Dezembro"
        ]

    def get_providers(self):
        return ["Total de Entregas Mensais"]

    def get_data(self):
        import datetime
        from django.db.models import Count
        from django.db.models.functions import TruncMonth
        from delivery.models import Delivery

        date = datetime.date.today()
        items = Delivery.objects.filter(date__year=date.year).annotate(month=TruncMonth('date')).values(
            'month').annotate(total=Count('id'))
        totalMonth = {}

        for i in range(0, 12):
            totalMonth[i] = '0'

        for item in items:
            month = item["month"]
            totalMonth[month.month]= item["total"]

        return [
        	[int(totalMonth.get(0)),
        	int(totalMonth.get(1)),
        	int(totalMonth.get(2)),
        	int(totalMonth.get(3)),
        	int(totalMonth.get(4)),
        	int(totalMonth.get(5)),
        	int(totalMonth.get(6)),
        	int(totalMonth.get(7)),
        	int(totalMonth.get(8)),
        	int(totalMonth.get(9)),
        	int(totalMonth.get(10)),
        	int(totalMonth.get(11))]
        ]

line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = TotalMonthlyDeliveries.as_view()