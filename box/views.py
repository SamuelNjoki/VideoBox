from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from box.forms import VideoForm

from box.models import Box

# Create your views here.

def home(request):
    return render(request,'box/home.html')

def dashboard(request):
    box=Box.objects.all()
    return render(request,'box/dashboard.html',{'box':box})

def addVideo(request,pk):
    form=VideoForm()
    context={
        'form':form
    }
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

