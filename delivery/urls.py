from django.urls import path
from .views import render_pdf

urlpatterns = [
    # path('pdf/', render_pdf, name='render_pdf'),
    path('pdf/<int:delivery_id>/', render_pdf, name='render_pdf'),
]
