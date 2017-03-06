from django import forms
from .models import Comment
from pagedown.widgets import PagedownWidget

#from dmlsite.fields import AddressField
from dmlsite.widgets import MyWidget


class CommentForm(forms.ModelForm):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
	text = forms.CharField(label="", widget=PagedownWidget(show_preview=False)) #(template=pagedown/widgets/default.html, css=("custom/css1.css", "custom/css2.css")
	#published_date = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model = Comment
		fields = ['text',]

class CommentReplyForm(forms.ModelForm):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
	text = forms.CharField(label="", widget=PagedownWidget(show_preview=False)) #(template=pagedown/widgets/default.html, css=("custom/css1.css", "custom/css2.css")
	#published_date = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model = Comment
		fields = ['text',]

class VisitorCommentForm(forms.ModelForm):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	text = forms.CharField(label="", widget=forms.Textarea)
	parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
	class Meta:
		model = Comment
		fields = ['visitor', 'text',]
