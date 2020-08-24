from django import forms
from .models import Question, Choice  # , Votes
from pagedown.widgets import PagedownWidget


class AddPollForm(forms.ModelForm):

    # object_id = forms.IntegerField(widget=forms.HiddenInput)
    question_text = forms.CharField(label="Question", widget=PagedownWidget())
    pub_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Question
        fields = ['question_text', ]  # "tags""image" add comment form

    def clean_question_text(self) -> str:
        question_text: str = self.cleaned_data.get('question_text')
        return question_text


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
