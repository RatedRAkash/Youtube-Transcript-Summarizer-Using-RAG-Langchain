import logging

from django.shortcuts import render
from django.views import View

from .forms import YoutubeTranscriptForm

logger = logging.getLogger(__name__)

# extends Normal Class-based `View`
class HomeView(View):
    view_name = 'home_view'
    template_name = 'home.html'

    def get(self, request):
        youtube_transcript_form = YoutubeTranscriptForm()

        context = {
            'youtube_transcript_form': youtube_transcript_form
        }

        return render(request, self.template_name, context)


    def post(self, request):
        form = YoutubeTranscriptForm(request.POST)

        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            user_query = form.cleaned_data['user_query']

            # Example context to show results
            context = {
                'youtube_transcript_form': form,
                'summary_result': f"Summary for '{user_query}' from {youtube_url}"  # dummy result
            }

            return render(request, self.template_name, context)

        # If the form is not valid, re-render with errors
        return render(request, self.template_name, {'youtube_transcript_form': form})