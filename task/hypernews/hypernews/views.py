from django.shortcuts import HttpResponse, redirect


def coming_soon(request):
    return redirect('/news/')
