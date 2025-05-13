import logging

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from ..forms import YoutubeTranscriptForm
from .utils import extract_youtube_video_id

from youtube_transcript_RAG_model.main import get_summary_main

logger = logging.getLogger(__name__)

class GetYoutubeTranscriptSummary(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]  # Allow access to all users, authenticated or not

    api_name = "api/get-summary"

    def post(self, request):
        form = YoutubeTranscriptForm(request.POST)

        if form.is_valid():
            youtube_url = form.cleaned_data['youtube_url']
            user_query = form.cleaned_data['user_query']

            # Do something with the submitted data (e.g., call your summary logic)
            logging.info("YouTube URL: " + youtube_url)
            logging.info("User Query: " + user_query)

            rag_summary = get_summary_main(extract_youtube_video_id(youtube_url), user_query)
            logging.info("=============Summary=============\n" + rag_summary)

            return Response({'summary': rag_summary}, status=status.HTTP_200_OK)

        # If the form is not valid, re-render with errors
        return Response({'summary': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)