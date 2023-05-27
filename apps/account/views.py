from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from .forms import LoginForm, ChangePasswordForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class LoginView(View):
    """Login to the platform"""
    form_class = LoginForm
    template_name = 'login.html'
    success_url = 'threads:lists'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            # authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                remember_me = request.POST.get("remember_me")
                if remember_me is True:
                    ONE_MONTH = 30 * 24 * 60 * 60
                    expiry = getattr(
                        settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
                    request.session.set_expiry(expiry)

                # redirect
                return redirect(self.success_url)
            else:
                messages.error(request, 'Wrong credentials, try again!')

       # render
        return render(request, self.template_name, {'form': form})

    
class ChangePasswordView(View):
    """Change Password"""
    template_name = 'change_password.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChangePasswordView, self).dispatch( *args, **kwargs)

    def get(self, request):
        form = ChangePasswordForm(request.user)
        context = {"form": form}

        """render view"""
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change-password')
        else:
            form = ChangePasswordForm(request.user)

        """render same form"""
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Logout class"""
    def get(self, request):
        logout(request)
        messages.error(request, 'Log out successfully')
        return redirect('login')