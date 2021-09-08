from django.shortcuts import redirect


def delivery_report(self, request, queryset):
	if queryset.count() > 1:
		return None

	for delivery in queryset:
		d_id = delivery.id

	return redirect('/pdf/' + str(d_id))
