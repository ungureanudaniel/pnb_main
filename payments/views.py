from django.shortcuts import render

def ticketpay_view(request):
    template = "payments/ticket-description.html"
    nr_pers = request.POST.get('nr_pers')
    print(nr_pers)
    context = {
        "nr_pers": nr_pers,
    }
    return render(request, template, context)

def checkout_view(request):
    template = "payments/ticket-checkout.html"

    context = {

    }
    return render(request, template, context)
