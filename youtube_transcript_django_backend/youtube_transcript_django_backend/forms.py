from django import forms

class YoutubeTranscriptForm(forms.Form):
    youtube_url = forms.URLField(
        label="YouTube Link:",
        widget=forms.URLInput(
            attrs={
                'id': 'youtubeLink',
                'name': 'youtubeLink',
                'required': True,
                'placeholder': 'Enter YouTube video URL',
                'class': 'form-control'
            }
        )
    )

    user_query = forms.CharField(
        label="Your Query:",
        widget=forms.TextInput(
            attrs={
                'id': 'query',
                'name': 'query',
                'required': True,
                'placeholder': 'Enter your question...',
                'class': 'form-control'
            }
        )
    )