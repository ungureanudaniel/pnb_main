from django.shortcuts import render
#========================bear awareness VIEW=================================
def bear_awareness(request):
    template = 'education/bear-awareness.html'
   
    context = {}
    return render(request, template, context)