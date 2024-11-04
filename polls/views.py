from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy
from .models import Question, Choice
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import UpdateView, CreateView, TemplateView, DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django import forms
from .models import AdvUser
from .forms import ChangeUserInfoForm
from django.core.signing import BadSignature
from django.views.generic import CreateView
from django.views.generic import TemplateView
from .forms import RegisterUserForm
from .utilities import signer

def base(request): 
    return render(request, 'base.html')


from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import RegisterUserForm  # Import your form here

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'user/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('polls:register_done')  # Adjusted success URL

class RegisterDoneView(TemplateView):
    template_name = 'user/register_done.html'



from django.views.generic import TemplateView
class RegisterDoneView(TemplateView):
   template_name = 'user/register_done.html'



def user_activate(request, sign):
   try:
       username = signer.unsign(sign)
   except BadSignature:
       return render(request, 'user/bad_signature.html')
   user = get_object_or_404(AdvUser, username=username)
   if user.is_activated:
       template = 'user/user_is_activated.html'
   else:
       template = 'user/activation_done.html'
       user.is_activated = True
       user.is_active = True
       user.save()
   return render(request, template)


class BBLoginView(LoginView): 
    template_name = 'user/login.html' 


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'user/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('polls:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def form_valid(self, form):
        return super().form_valid(form)



@login_required 
def profile(request): 
        return render(request, 'user/profile.html')



class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('polls:base')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    

class BBLogoutView(LoginRequiredMixin, LogoutView): 
   template_name = 'user/logout.html' 


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific question and choices


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

# Get question and display results


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Vote for a question choice


def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
