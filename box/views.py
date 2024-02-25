from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from box.forms import SearchForm, VideoForm
from box.models import Box, Video
import urllib
from django.forms.utils import ErrorList

# Create your views here.
YOUTUBE_API_KEY='AIzaSyDFHl8bhkTqVa7Jad4P_6gT9pKFxKTVZWU'

def home(request):
    return render(request,'box/home.html')

def dashboard(request):
    box=Box.objects.all()
    return render(request,'box/dashboard.html',{'box':box})

def addVideo(request,pk):
    form=VideoForm()
    s_form=SearchForm()
    box=Box.objects.get(id=pk)
    context={
        'form':form,
        's_form':s_form,
        'box':box
    }
    if not box.user==request.user:
        raise Http404
    
    if request.method=='POST':
        filled_form=VideoForm(request.POST)
        if filled_form.is_valid():
            video=Video()
            # video.title=filled_form.cleaned_data['title']
            # video.youtube_id=filled_form.cleaned_data['youtube_id']
            video.url=filled_form.cleaned_data['url']
            parsed_url=urllib.parse.urlparse(video.url)
            video_id=urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id=video_id[0]
                
                video.box=box
                video.save()
    return render(request,'box/addvideo.html',context)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name= "registration/signup.html"
    
    def form_valid(self, form):
        view=super(SignUp,self).form_valid(form)
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password1')
        user=authenticate(username=username, password=password)
        login(self.request,user)
        return view
class LogOut(generic.View):
    def get(self, request):
        logout(request) 
        return redirect('home')

class CreateBox(generic.CreateView):
    model=Box
    fields=['title']
    template_name='box/create_box.html'
    success_url=reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        super(CreateBox,self).form_valid(form)
        return redirect('home')
    
    
class ListBox(generic.ListView):
    model=Box
    template_name='box/listbox.html'
    
class DetailBox(generic.DetailView):
    model=Box
    template_name='box/detailbox.html'


class UpdateBox(generic.UpdateView):
    model=Box
    template_name='box/updatebox.html'
    fields=['title']
    success_url=reverse_lazy('dashboard')

class DeleteBox(generic.DeleteView):
    model=Box
    template_name='box/deletebox.html'
    success_url=reverse_lazy('dashboard')

