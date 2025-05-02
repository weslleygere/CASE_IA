from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404

from django.contrib import messages

from django.urls import reverse, reverse_lazy

from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView

from .forms.login import UserLoginForm
from .forms.register import UserRegisterForm
from .forms.edit import UserEditForm
from .forms.reset_password_request import PasswordResetForm
from .forms.reset_password_change import PasswordChangeForm

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login' 

class UserRegisterView(LoginRequiredMixin, FormView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        form.save() 
        return super().form_valid(form) 

class UserEditView(LoginRequiredMixin, FormView):
    form_class = UserEditForm
    template_name = 'users/edit.html'
    success_url = reverse_lazy('user_list')  

    def dispatch(self, request, *args, **kwargs):
        self.target_user = get_object_or_404(User, pk=kwargs.get('pk', request.user.pk))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.target_user 
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.target_user  # Já existente
        back_url = self.request.GET.get('next') or self.request.META.get('HTTP_REFERER') or reverse('user_list')
        context['back_url'] = back_url
        return context

    def form_valid(self, form):
        user = form.save()

        if user == self.request.user:
            update_session_auth_hash(self.request, user)

        return super().form_valid(form)
    
class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        target_user = User.objects.get(pk=pk)

        if target_user.is_superuser:
            messages.error(request, "Usuário administrador não pode ser excluído.")
            return redirect('user_list')

        if target_user == request.user:
            target_user.delete()
            logout(request)
            return redirect('login')  
        else:
            target_user.delete()
            messages.success(request, "Usuário excluído com sucesso.")
            return redirect('user_list')

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

class UserSearchView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_search.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(username__icontains=q) | queryset.filter(email__icontains=q)
        return queryset 
    
class PasswordRequestView(FormView):
    form_class = PasswordResetForm
    template_name = 'users/reset_password_request.html'
    success_url = reverse_lazy('reset_password_request')

    def form_valid(self, form):
        if form.send_reset_email(self.request):
            messages.success(self.request, form.success_message)
        else:
            messages.error(self.request, form.error_message)
        return super().form_valid(form)

class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'users/reset_password_change.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        form = self.get_form()
        
        if not form.is_valid_token():
            messages.error(request, form.error_message)
            return redirect('reset_password_request')
        self.valid_user = form.user
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['uidb64'] = self.kwargs.get("uidb64")
        kwargs['token'] = self.kwargs.get("token")
        kwargs["user"] = getattr(self, 'valid_user', None)
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, form.success_message)
        return super().form_valid(form)
