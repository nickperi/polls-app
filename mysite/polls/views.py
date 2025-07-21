from django.db.models import F, Subquery
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.utils import timezone

from .models import Voter, Choice, Question, User_Question

# Create your views here.
class IndexView(generic.TemplateView):
    #context_object_name = "latest_question_list"
    template_name = "polls/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answered_question_ids = User_Question.objects.values('question')

        context['answered_question_list'] = Question.objects.filter(id__in=Subquery(answered_question_ids), pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        context['unanswered_question_list'] = Question.objects.exclude(id__in=Subquery(answered_question_ids), pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

        return context

    '''def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5] '''

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
   model = Question
   template_name = "polls/results.html"



def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            current_user=Voter.objects.get(email=email)
            return redirect('index')
            # Redirect to a success page.
        else:
            messages.success(request, ("Invalid username or password... Try again !"))
            return redirect('/polls/login_user')
    else:
        return render(request, 'polls/login.html')

def logout_user(request):
    logout(request)
    return redirect('/polls/login_user')


@login_required
def vote(request, question_id, user_id):
    question = get_object_or_404(Question, pk=question_id)
    user = get_object_or_404(Voter, pk=user_id)
    
    try:
        voted = User_Question.objects.get(user=user, question=question)
    except User_Question.DoesNotExist:
        voted = None

    try:
        if voted is None:
            if user:
                selected_choice = question.choice_set.get(pk=request.POST["choice"])
                user_question = User_Question(user=user, question=question)
                user_question.save()
                messages.success(request, 'Your vote was successful!')
        else:
            messages.success(request, 'You already voted on this question!')
            return redirect('/polls/' + str(question_id) +'/results/')

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
