from django.shortcuts import render

def ticketpay_view(request):
    template = "payments/ticket-description.html"
    context = {}
    if request.method=="POST":
        try:
            pers = request.POST.get('total')
            print(f"{pers}")
            context = {
                "nr_pers": pers,
            }
        except Exception as e:
            print(f"Error:{e}!")
    else:
        print("Post request not working!")
    return render(request, template, context)

def checkout_view(request):
    template = "payments/ticket-checkout.html"

    context = {

    }
    return render(request, template, context)
