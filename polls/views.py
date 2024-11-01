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
from django.contrib.auth.views import LogoutView
from django import forms
from .models import AdvUser


def base(request): 
    return render(request, 'base.html')


class BBLoginView(LoginView): 
    template_name = 'user/login.html' 

    
@login_required 
def profile(request): 
        return render(request, 'user/profile.html')

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
