from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView  # a view that returns back info on a single item it works based on id or pk.
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView # formview is a view for creaating a form and rendering template response
from django.contrib.auth.forms import UserCreationForm #a form that creates a user for us.(bulitIn)
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Task
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin



class Register(FormView):
    template_name = "base/register.html" #where our template is.
    form_class = UserCreationForm # we choose type of form we want for our register page here
    #redirect_authenticated_user = True
    success_url= reverse_lazy("tasks")
    
    def form_valid(self, form):
        user = form.save()
        if user is not None: # translation if saved successfully
            login(self.request, user) # login user
        return super(Register, self).form_valid(form)
    
    def get(self, *args, **kwargs): #redirect_authenticated_user = True had to override so created this function
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(Register, self).get(*args, **kwargs)
    
    
class Login(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True #an authenticated user can't get to the login page
    
    def get_success_url(self):
        return reverse_lazy("tasks")
    
    

class Task_list(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks" # class based view was formerly looking for "object_list" changed it to "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["tasks"] = context ["tasks"].filter(user=self.request.user) #the side before the = is a variable the side after the equal to symbol is the yalue. The value in this case is our tasks filtered based on self.request user
        context ["count"] = context ["tasks"].filter(complete=False).count() # here we filter context  based on False task(incomplete tasks) count

        search_input= self.request.GET.get("q") or ''
        if search_input: # translation if we have search data here
            context["tasks"] = context ["tasks"].filter(title__icontains=search_input) #filter based on search input that contains title
                                                                                       #PS if you want to search from the start of the word or sentence first use /
                                                                                       #title__startswith instead   
        return context
    
    
class Task_detail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"# class based view was formerly looking for "object" changed it to "task"
    template_name = "base/task.html" # on default looking for template "task_detail".changed by directing to task.html
    
class Create_task(LoginRequiredMixin, CreateView): # by default createview uses modelform Ps in template it looks for task_form
    model = Task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("tasks") 
    
    def form_valid(self, form):
        form.instance.user = self.request.user# form when we create task in this instance has to be = the request.user
        return super(Create_task, self).form_valid(form)
    
class Update_task(LoginRequiredMixin, UpdateView):  # also looks for template with suffix as model form (task) and prefix as (form).
    model = Task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("tasks") 

class Delete_task(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "tasks"
    template_name = "base/delete.html"
    success_url = reverse_lazy("tasks")
    

    