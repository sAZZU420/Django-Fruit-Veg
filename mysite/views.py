from django.shortcuts import render


def handle_404(request, exception):
    return render(request, '404_page.html')
