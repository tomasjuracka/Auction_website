from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from profiles.models import Profile


# Create your views here.

def profiles_list(request):
    users_list = User.objects.all()

    context = {'users': users_list}
    return render(request, 'profiles/users.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    context = {'profile': profile}
    return render(request, "profiles/user.html", context)


@login_required
def create_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        city = request.POST.get('city').strip()
        address = request.POST.get('address').strip()
        file_url = ""
        if request.FILES.get('upload'):
            upload = request.FILES['upload']
            file_storage = FileSystemStorage()
            file = file_storage.save(upload.name, upload)
            file_url = file_storage.url(file)

        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        profile = Profile.objects.create(
            user=user,
            city=city,
            address=address,
            photo=file_url,
        )
        profile.favorites_set()
        return redirect('profiles')
    return render(request, 'profiles/create_profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        city = request.POST.get('city').strip()
        address = request.POST.get('address').strip()
        file_url = ""
        if request.FILES.get('upload'):
            upload = request.FILES['upload']
            file_storage = FileSystemStorage()
            file = file_storage.save(upload.name, upload)
            file_url = file_storage.url(file)

        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        user.userprofile.city = city
        user.userprofile.address = address
        user.userprofile.photo = file_url
        user.userprofile.save()
        profile = user.userprofile

        return redirect('profiles')
    user = User.objects.get(id=request.user.id)
    profile = user.userprofile
    context = {"profile": profile}
    return render(request, 'profiles/edit_user.html', context)
