from django.shortcuts import render

def about_us(request):
    """ A view to show the about us page """
    return render(request, 'about/about_us.html')

def sustainability_pledge(request):
    """ A view to show the sustainability pledge page """
    return render(request, 'about/sustainability_pledge.html')

def connect_with_us(request):
    """ A view to show the connect with us page """
    return render(request, 'about/connect_with_us.html')

