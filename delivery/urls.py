from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import render_pdf, TotalMonthlyDeliveries

urlpatterns = [
    # path('pdf/', render_pdf, name='render_pdf'),
    path('pdf/<int:delivery_id>/', login_required(render_pdf), name='render_pdf'),
    path('chart/total_deliveries/', TotalMonthlyDeliveries.as_view(), name='total_deliveries')
]
