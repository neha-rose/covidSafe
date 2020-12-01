from django.shortcuts import render

# Create your views here.
def welcomepage(request):
    return render(request, "main/welcome.html", {})