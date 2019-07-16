from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views import generic
from django.views.generic import View
from .models import Album,Song
from .forms import Userform

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','release','album_logo']
    success_url = "/music/"


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist','album_title','genre','release','album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongCreate(CreateView):
    model = Song
    fields = ['album','file_type','song_title','is_favorite']
    success_url = "/music/{album_id}"


class UserFormView(View):
    form_class = Userform
    template_name = 'music/registration_form.html'

    #get means a blank form which requires to be filled if it is a new user i.e,Register
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data after clicking on submit
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # clean (normalized) data
            username = form.cleaned_data['username']

            password = form.cleaned_data['password']
            # set the user password beçause password should be in the form of hash
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username,password=password)

            if user:

                if user.is_active:
                    login(request,user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})
