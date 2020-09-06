from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings 
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from .models import Profile, Connect, VerifyInfo
from django.http import Http404 
from .forms import ProfileEditForm, VerificationInfoForm, VerificationTokenForm
from authy.api import AuthyApiClient 

import requests 

class ConnectionsView(LoginRequiredMixin, View): 

    template_name = 'users/connect.html'

    def get(self, request, *args, **kwargs): 
        try: 
            all_choices = Connect.objects.all().filter(user=request.user).values() 

            users = User.objects.all().exclude(
                id=request.user.id
            )
    
            for user in users: 
                for info in all_choices: 
                    if request.user.id == info.get('user_id', False) and user.id == info.get('other_user_id', False):
                        users = users.exclude(id=user.id)

        except Exception as e: 
            users = None 

        context = {
            'users': users,
            }

        return render(request, self.template_name, context=context)

    @classmethod 
    def process_request(cls, request, user_id, add):

        try: 
            other_user = User.objects.get(id=user_id)

            Connect.objects.get_or_create(
                user=request.user, 
                other_user = other_user, 
                connect = add, 
            )
            
            if add and Connect.objects.filter(
                user=other_user, 
                other_user=request.user,
                connect = True,
            ).count():

                from_user = Connect.objects.get(user=request.user, other_user=other_user)
                to_user = Connect.objects.get(user=other_user, other_user=request.user)
                from_user.connected = True 
                to_user.connected = True 
                from_user.save()
                to_user.save() 

                context = {
                    'match': other_user, 
                }

                return render(request, 'users/match.html', context=context) 

        except IndexError:
            context = {} # placeholder to pass error 

        return redirect('connect_find')
    
    @classmethod 
    def add(cls, request, user_id): 
        return cls.process_request(request, user_id, True)

    @classmethod 
    def reject(cls, request, user_id): 
        return cls.process_request(request, user_id, False)

class ProfileView(LoginRequiredMixin, View): 

    template_name = 'users/profile.html'

    def get(self, request, user_id=False): 
        try: 
            if not user_id: 
                user_id = request.user.id 

            user = User.objects.get(id=user_id) 

            profile = Profile.objects.get(user=user)

            context = {
                'profile': profile,
            }

            return render(request, self.template_name, context=context)

        except Exception as e:
            print(e) 
            raise Http404('Oops. Something went wrong!')

class ProfileEditView(LoginRequiredMixin, View):

    template_name = 'users/profile_edit.html'
    form_class = ProfileEditForm

    def get(self, request, *args, **kwargs): 
        form = self.form_class(instance=request.user.profile)

        context = {
            'form': form, 
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs): 

        form = self.form_class(request.POST, request.FILES or None, instance=request.user.profile)

        if form.is_valid():

            verify_form = VerificationInfoForm(instance=request.user.verifyinfo)

            if verify_form.is_valid(): 
                verify_form.profile_complete = True 
                verify_form.save()

            form.save()

            return redirect('profile')

        context = {
            'form': form,
        }

        return render(request, self.template_name, context=context)

class VerificationView(LoginRequiredMixin, View): 

    template_name = 'users/verification.html'
    form_class = VerificationInfoForm
    authy_api = AuthyApiClient(settings.AUTHENTICATION_KEY)

    def get(self, request, *args, **kwargs): 

        form = self.form_class(instance=request.user.verifyinfo) 

        context = {
            'form': form,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs): 

        error = "Oops. Something went wrong."

        try: 

            form = self.form_class(request.POST, instance=request.user.verifyinfo) 

            if form.is_valid():

                form.save()
                
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                via = form.cleaned_data['via']
                country_code = form.cleaned_data['country_code']

                request.session['phone_number'] = phone_number 
                request.session['country_code'] = country_code 

                self.authy_api.phones.verification_start(
                    phone_number=phone_number, 
                    country_code=country_code, 
                    via=via, 
                )

                request.session['verify_started'] = True 

                return redirect('verify_otp')

            raise Exception 

        except Exception as e: 
            
            print(e)

            context = {
                'form': form,
                'error': error, 
            }

        return render(request, self.template_name, context=context)

class VerificationTokenView(LoginRequiredMixin, View): 

    template_name = 'users/verification_token.html'
    form_class = VerificationTokenForm
    authy_api = AuthyApiClient(settings.AUTHENTICATION_KEY)

    def get(self, request, *args, **kwargs): 
        try: 
            form = self.form_class() 

            context = {
                'form': form, 
            }

            if not request.session['verify_started']: raise Exception('verify not started')

            return render(request, self.template_name, context=context)

        except Exception as e:
            print(e)

            redirect('verify_setup')

    def post(self, request, *args, **kwargs): 

        error = "Oop. Something went wrong."

        try: 
            form = self.form_class(request.POST)

            if form.is_valid(): 

                token = form.cleaned_data['token']

                verification = self.authy_api.phones.verification_check(
                    request.session['phone_number'],
                    request.session['country_code'],
                    token
                )

                if verification.ok(): 

                    profile = ProfileEditForm(instance=request.user.profile)

                    if profile.is_valid(): 

                        profile.phone_number_verified = True 

                        profile.save() 

                    request.session['verification'] = True 

                    return redirect('verify_success')

                else: 
                    error = ' '.join([error for error in verification.errors()])
                
            raise Exception('Form invalid.')

        except Exception as e:

            print(e) 

            context = {
                'form': form, 
                'error': error, 
            }
        
            return render(request, self.template_name, context=context)

class VerificationSuccessView(LoginRequiredMixin, View): 

    template_name = "users/verification_success.html"

    def get(self, request, *args, **kwargs): 
        try: 

            if request.session['verification']: 
                return render(request, self.template_name)

            raise Exception 

        except: 
            return redirect('verify_setup')