from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
def ticketpay_view(request):
    template = "payments/ticket-online.html"
    context = {}
    if request.method=="POST":
        try:
            pers = request.POST.get('total')
            context = {
                "nr_pers": pers,
            }
        except Exception as e:
            messages.warning(request, _(f"Failed! {e}"))
    else:
        messages.warning(request, _(f"Failed! Try again or contact us."))
    return render(request, template, context)

def checkout_view(request):
    template = "payments/ticket-checkout.html"

    context = {

    }
    return render(request, template, context)
