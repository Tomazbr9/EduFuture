from django.shortcuts import render


def profile_view(request, name_user):
    return render(request, 'profile.html')