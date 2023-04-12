from django.shortcuts import render

def ticketpay(request):
    template = "pnb_main/ticket-description.html"

    context = {

    }
    return render(request, template, context)
