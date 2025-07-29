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
def index_view(request):
    #context_object_name = "latest_question_list"
    template_name = "polls/index.html"

    auth_navigation_bar = [('/', 'index', 'Home'), ('/polls/profile/'+str(request.user.id), 'profile', 'My Profile'), ('/polls/logout_user', 'logout', 'Logout')]
    navigation_bar = [('/', 'index', 'Home'), ('/polls/login_user', 'login', 'Login')]
    active_page = 'index'

    context = {'navigation_bar':navigation_bar, 'auth_navigation_bar':auth_navigation_bar, 'active_page':active_page}

    '''def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5] '''
    return render(request, template_name, context)

def profile_view(request, user_id):
    template_name = "polls/profile.html"
    answered_question_ids = User_Question.objects.filter(user_id=user_id).values('question')
    answered_question_list = Question.objects.filter(id__in=Subquery(answered_question_ids), pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    unanswered_question_list = Question.objects.exclude(id__in=Subquery(answered_question_ids), pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    auth_navigation_bar = [('/', 'index', 'Home'), ('/polls/profile/'+str(request.user.id), 'profile', 'My Profile'), ('/polls/logout_user', 'logout', 'Logout')]
    navigation_bar = [('/', 'index', 'Home'), ('/polls/login_user', 'login', 'Login')]
    context = {'answered_question_list':answered_question_list, 'unanswered_question_list': unanswered_question_list, 'navigation_bar':navigation_bar, 'auth_navigation_bar':auth_navigation_bar}
    return render(request, template_name, context)

   
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def results_view(request, user_id, question_id):
   template_name = "polls/results.html"
   question = get_object_or_404(Question, pk=question_id)
   my_vote = get_object_or_404(User_Question, user_id=user_id, question_id=question_id)
   my_choice = get_object_or_404(Choice, pk=my_vote.choice_id)
   context = {'my_choice': my_choice, 'question':question}
   return render(request, template_name, context)

    


def choice_view(request, choice_id):
    choice = Choice.objects.get(id=choice_id)
    votes = choice.user_question_set.all()
    voters = []

    for vote in votes:
        voters.append(Voter.objects.get(id=vote.user_id).first_name + " " + " " + Voter.objects.get(id=vote.user_id).last_name)

    context = {'choice': choice, 'voters':voters}
    return render(request, 'polls/choice.html', context)
        



def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            current_user=Voter.objects.get(email=email)
            return redirect('/polls/profile/' + str(user.id))
            # Redirect to a success page.
        else:
            messages.success(request, ("Invalid username or password... Try again !"))
            return redirect('/polls/login_user')
    else:
        return render(request, 'polls/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')


@login_required
def vote(request, question_id, user_id):
    question = get_object_or_404(Question, pk=question_id)
    user = get_object_or_404(Voter, pk=user_id)
    
    try:
        vote = User_Question.objects.get(user=user, question=question)
    except User_Question.DoesNotExist:
        vote = None

    try:
        if user: 
            if vote is None:
                selected_choice = question.choice_set.get(pk=request.POST["choice"])
                user_question = User_Question(user=user, question=question, choice=selected_choice)
                user_question.save()
                selected_choice.votes = F("votes") + 1
                selected_choice.save()
                messages.success(request, 'Your vote was successful!')
                
            else:
                prev_selected_choice = vote.choice
                selected_choice = question.choice_set.get(pk=request.POST["choice"])

                if selected_choice.choice_text == prev_selected_choice.choice_text:
                    messages.success(request, 'You already voted for this choice!')
                else:
                    prev_selected_choice.votes = F("votes") - 1
                    prev_selected_choice.save()
                    vote.choice = selected_choice
                    vote.save()
                    selected_choice.votes = F("votes") + 1
                    selected_choice.save()
                    messages.success(request, 'Your vote was successfully updated!')
      
        
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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        return HttpResponseRedirect(reverse("polls:results", args=(question.id, user_id)))
        
