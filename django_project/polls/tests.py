import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# TODO: rewrite with pytest maybe?

class QuestionModelTests(TestCase):
    """Contains tests specific for Question Model"""

    def test_is_recent_with_future_date(self):
        """
        is_recent() returns False for questions whose dt_published
        is in the future.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(dt_published=time)
        self.assertIs(future_question.is_recent(), False)

    def test_is_recent_with_old_question(self):
        """
        is_recent() returns False for questions whose dt_published
        is older than 1 day.
        """

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(dt_published=time)
        self.assertIs(old_question.is_recent(), False)

    def test_is_recent_with_recent_question(self):
        """
        is_recent() returns True for questions whose dt_published
        is within the last day.
        """

        now = timezone.now()
        time = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(dt_published=time)
        self.assertIs(recent_question.is_recent(), True)


def create_question(text, days):
    """
    Create a question with the given `text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(text=text, dt_published=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a dt_published in the past are displayed on the
        index page.
        """

        create_question(text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a dt_published in the future aren't displayed on
        the index page.
        """

        create_question(text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """

        create_question(text="Past question.", days=-30)
        create_question(text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""

        create_question(text="Past question 1.", days=-30)
        create_question(text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a dt_published in the future
        returns a 404 not found.
        """
        future_question = create_question(text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a dt_published in the past
        displays the question's text.
        """

        past_question = create_question(text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.text)