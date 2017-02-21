from django import forms
from .models import Comment
from pagedown.widgets import PagedownWidget


class CommentForm(forms.ModelForm):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	text = forms.CharField(widget=forms.Textarea)
	#parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
	#text = forms.CharField(widget=PagedownWidget(show_preview=True)) #(template=pagedown/widgets/default.html, css=("custom/css1.css", "custom/css2.css")
	#published_date = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model = Comment
		fields = ('author', 'text',)
