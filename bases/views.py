from django.shortcuts import render, redirect
from django.views import View 
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

class LandingView(View): 
    template_view = 'bases/landing.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_view)

class RegisterView(View): 
    form_class = RegisterForm
    template_name = 'bases/register.html'
    success_message = "For extra security, a verification code has been sent to your mobile number."
    # success_url 

    def get(self, request, *args, **kwargs): 
        """
        Want to implement the register form 
        """

        form = self.form_class() 

        context = {'form': form,}

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs): 

        form = RegisterForm(request.POST)

        context = {'form': form,}

        if form.is_valid(): 
            form.save()

            return redirect('login')
        
        return render(request, self.template_name, context=context)