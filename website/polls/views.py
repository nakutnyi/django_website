"""
This file contains views.

From Django docs: A view is a "type" of Web page in your Django application
that generally serves a specific function and has a specific template.
"""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """

        questions = Question.objects.filter(dt_published__lte=timezone.now())

        return questions.order_by('-dt_published')[:5]


class DetailView(generic.DetailView):
    """Question voting details view"""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""

        return Question.objects.filter(dt_published__lte=timezone.now())


class ResultsView(generic.DetailView):
    """View question results"""

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Vote view"""

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
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


