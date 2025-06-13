import datetime
import io
import json
import logging
import os
import uuid

import matplotlib
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from matplotlib import pyplot as plt

from wordcloud_project.custom_azure import AzureMediaStorage


logger = logging.getLogger(__name__)

matplotlib.use('Agg')  # Use non-interactive backend
from wordcloud import WordCloud as WC
from PIL import Image
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import openai
from .models import WordCloud, UserCredit
from .serializers import (
    WordCloudSerializer,
    WordCloudGenerateSerializer,
    WordCloudExportSerializer,
    AIWordSuggestionsSerializer,
    UserCreditSerializer
)

# Configure OpenAI API
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def run_prompt_gpt4mini(request, prompt, wordCount=100):
    if prompt == "" or prompt is None:
        return "Prompt is empty."

    response = client.responses.create(
        model="gpt-4o-mini",
        # input=[{"role": "user", "content": f"Generate {wordCount} words for a word cloud using the foollowing theme or suggestion: {prompt}"}],
        input=[{"role": "system",
                "content": (
                    f"Generate a list of {wordCount} words or short phrases related to the topic. "
                    f"Return only the Python list, with no extra formatting, no markdown, and no code block. "
                    f"Do not wrap the list in triple backticks or label it as code. Just output the list directly."
                )},
               {"role": "user", "content": f"Topic: {prompt}"}],
        text={
            "format": {
                "type": "text"
            }
        },
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=False
    )
    print("GPT-4 Mini response:", response.output_text)
    return response.output_text


def get_file_path(folder: str = None, filename: str = None) -> str:
    """
    Generate a structured file path using an optional folder and filename.
    """
    if folder is None:
        folder = datetime.date.today().strftime("%Y/%m")

    if filename is None or '.' not in filename:
        filename = f"{uuid.uuid4()}.png"  # default to PNG

    return os.path.join(folder, filename)


def save_pil_image_to_azure(image, folder: str = None, filename: str = None) -> str:
    """
    Save a PIL image (e.g., from Matplotlib or WordCloud) to Azure using Django's default storage.
    Returns the full accessible URL to the file.
    """
    # Save image to memory
    img_io = io.BytesIO()
    image.save(img_io, format='PNG')
    img_content = ContentFile(img_io.getvalue())

    # Create file path
    filepath = get_file_path(folder, filename)

    # Save to Azure via Django storage
    fs = AzureMediaStorage()
    saved_path = fs.save(filepath, img_content)
    return fs.url(saved_path)


class WordCloudListCreateView(generics.ListCreateAPIView):
    """API view to list and create word clouds"""
    serializer_class = WordCloudSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only word clouds belonging to the current user"""
        return WordCloud.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating a new word cloud"""
        serializer.save(user=self.request.user)


class WordCloudDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update and delete word clouds"""
    serializer_class = WordCloudSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only word clouds belonging to the current user"""
        return WordCloud.objects.filter(user=self.request.user)


class GenerateWordCloudView(APIView):
    """API view to generate a word cloud"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WordCloudGenerateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Check if AI-generated and if user has enough credits
        if data['is_ai_generated']:
            user_credit = UserCredit.objects.get(user=request.user)
            if user_credit.credits_remaining <= 0:
                return Response(
                    {'error': 'You have no AI credits remaining. Please purchase more credits.'},
                    status=status.HTTP_402_PAYMENT_REQUIRED
                )

            # Deduct credit
            user_credit.credits_remaining -= 1
            user_credit.save()

        try:
            # Generate word cloud image using matplotlib
            wordcloud_img = self._generate_wordcloud_matplotlib(data)

            # Upload to Azure Blob Storage (only image)
            image_url = save_pil_image_to_azure(wordcloud_img, folder='wordclouds')

            # Create and save WordCloud model
            wordcloud = WordCloud.objects.create(
                user=request.user,
                title=data['title'],
                input_text=data['input_text'],
                is_ai_generated=data['is_ai_generated'],
                width=data['width'],
                height=data['height'],
                font=data['font'],
                color_scheme=data['color_scheme'],
                background_color=data['background_color'],
                max_words=data['max_words'],
                word_density=data['word_density'],
                orientation=data['orientation'],
                image_url=image_url,
                svg_url=None
            )

            print("Word cloud saved to database.", wordcloud)

            # Return the created word cloud data
            return Response(WordCloudSerializer(wordcloud).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # If an error occurs, refund the credit if it was deducted
            if data.get('is_ai_generated', False):
                user_credit = UserCredit.objects.get(user=request.user)
                user_credit.credits_remaining += 1
                user_credit.save()

            return Response(
                {'error': f'Failed to generate word cloud: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _generate_wordcloud_matplotlib(self, data):
        """Generate word cloud using matplotlib and return PIL Image"""
        # Configure word cloud
        colormap = data['color_scheme'] if data['color_scheme'] != 'default' else None

        wordcloud = WC(
            width=data['width'],
            height=data['height'],
            background_color=data['background_color'],
            max_words=data['max_words'],
            prefer_horizontal=1.0 if data['orientation'] == 'horizontal' else
            0.0 if data['orientation'] == 'vertical' else 0.5,
            scale=data['word_density'] / 50,
            font_path=f"fonts/{data['font']}.ttf" if os.path.exists(f"fonts/{data['font']}.ttf") else None,
            colormap=colormap
        ).generate(data['input_text'])

        # Create matplotlib figure
        plt.figure(figsize=(data['width'] / 100, data['height'] / 100), dpi=100)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(data['title'], fontsize=16)
        plt.axis("off")
        plt.tight_layout(pad=0)

        # Save to BytesIO buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='PNG', bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()  # Important: close the figure to free memory

        # Convert to PIL Image
        img_buffer.seek(0)
        pil_image = Image.open(img_buffer)

        return pil_image

    def _generate_wordcloud(self, data):
        """Generate word cloud image and SVG from input text (DEPRECATED - keeping for reference)"""
        # Convert word density to relative scale
        scale = data['word_density'] / 100

        # Configure word cloud
        wordcloud = WC(
            width=data['width'],
            height=data['height'],
            background_color=data['background_color'],
            max_words=data['max_words'],
            prefer_horizontal=1.0 if data['orientation'] == 'horizontal' else
            0.0 if data['orientation'] == 'vertical' else 0.5,
            scale=scale * 2,
            font_path=f"fonts/{data['font']}.ttf" if os.path.exists(f"fonts/{data['font']}.ttf") else None,
            colormap=data['color_scheme'] if data['color_scheme'] != 'default' else None
        )

        # Generate the word cloud
        wordcloud.generate(data['input_text'])

        # Convert to image
        wordcloud_img = wordcloud.to_image()

        # Generate SVG
        svg_data = wordcloud.to_svg()

        return wordcloud_img, svg_data


class WordCloudExportView(APIView):
    """API view to export a word cloud in different formats"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            # Get the word cloud
            wordcloud = WordCloud.objects.get(pk=pk, user=request.user)
        except WordCloud.DoesNotExist:
            return Response(
                {'error': 'Word cloud not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WordCloudExportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        export_format = serializer.validated_data['format']
        resolution = serializer.validated_data['resolution']

        try:
            # Regenerate the word cloud with the requested resolution
            if export_format == 'png':
                # Get resolution multiplier
                resolution_multiplier = {
                    'low': 1,
                    'medium': 2,
                    'high': 4
                }[resolution]

                # Regenerate word cloud with higher resolution
                width = wordcloud.width * resolution_multiplier
                height = wordcloud.height * resolution_multiplier

                # Generate word cloud
                wc_obj = WC(
                    width=width,
                    height=height,
                    background_color=wordcloud.background_color,
                    max_words=wordcloud.max_words,
                    prefer_horizontal=1.0 if wordcloud.orientation == 'horizontal' else
                    0.0 if wordcloud.orientation == 'vertical' else 0.5,
                    scale=wordcloud.word_density / 50 * resolution_multiplier,
                    font_path=f"fonts/{wordcloud.font}.ttf" if os.path.exists(f"fonts/{wordcloud.font}.ttf") else None,
                    colormap=wordcloud.color_scheme if wordcloud.color_scheme != 'default' else None
                )

                wc_obj.generate(wordcloud.input_text)
                img = wc_obj.to_image()

                # Prepare response
                response = HttpResponse(content_type="image/png")
                response['Content-Disposition'] = f'attachment; filename="{wordcloud.title}.png"'
                img.save(response, format="PNG")
                return response

            elif export_format == 'svg':
                # Generate word cloud
                wc_obj = WC(
                    width=wordcloud.width,
                    height=wordcloud.height,
                    background_color=wordcloud.background_color,
                    max_words=wordcloud.max_words,
                    prefer_horizontal=1.0 if wordcloud.orientation == 'horizontal' else
                    0.0 if wordcloud.orientation == 'vertical' else 0.5,
                    scale=wordcloud.word_density / 50,
                    font_path=f"fonts/{wordcloud.font}.ttf" if os.path.exists(f"fonts/{wordcloud.font}.ttf") else None,
                    colormap=wordcloud.color_scheme if wordcloud.color_scheme != 'default' else None
                )

                wc_obj.generate(wordcloud.input_text)
                svg_data = wc_obj.to_svg()

                # Prepare response
                response = HttpResponse(content_type="image/svg+xml")
                response['Content-Disposition'] = f'attachment; filename="{wordcloud.title}.svg"'
                response.write(svg_data)
                return response

        except Exception as e:
            return Response(
                {'error': f'Failed to export word cloud: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AIWordSuggestionsView(APIView):
    """API view to get word suggestions from OpenAI"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIWordSuggestionsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check if user has enough credits
        user_credit = UserCredit.objects.get(user=request.user)
        if user_credit.credits_remaining <= 0:
            return Response(
                {'error': 'You have no AI credits remaining. Please purchase more credits.'},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        topic = serializer.validated_data['topic']
        count = serializer.validated_data['count']

        try:
            # Make request to OpenAI API
            messages = [
                {"role": "system",
                 "content": f"Generate {count} words or short phrases related to the topic. Return them as a JSON array of strings. Make the words varied in frequency and relevance, like you would see in a natural word cloud."},
                {"role": "user", "content": f"Topic: {topic}"}
            ],

            # Parse the response
            response_text = run_prompt_gpt4mini(request, topic, count)

            # Try to extract JSON array from the response
            try:
                # If the response is already a valid JSON array
                words = json.loads(response_text)
                if not isinstance(words, list):
                    raise ValueError("Response is not a list")
            except json.JSONDecodeError:
                # If the response contains text around the JSON, try to extract it
                import re
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if json_match:
                    try:
                        words = json.loads(json_match.group(0))
                    except json.JSONDecodeError:
                        # If still can't parse, fall back to splitting by comma or newline
                        words = [w.strip().strip('"\'[]') for w in response_text.replace('\n', ',').split(',')]
                else:
                    # Fall back to splitting by comma or newline
                    words = [w.strip().strip('"\'[]') for w in response_text.replace('\n', ',').split(',')]

            # Filter out any empty strings
            words = [word for word in words if word]

            # Deduct credit
            user_credit.credits_remaining -= 1
            user_credit.save()

            # Create a string with frequency weights (repeating important words)
            weighted_words = []
            for word in words:
                # Add the word 1-5 times based on a simple random distribution
                # This simulates frequency/importance
                import random
                weight = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.3, 0.1, 0.07, 0.03])[0]
                weighted_words.extend([word] * weight)

            # Join with spaces to create a text string
            text = ' '.join(weighted_words)

            return Response({
                'words': words,
                'text': text,
                'credits_remaining': user_credit.credits_remaining
            })

        except Exception as e:
            # If an error occurs, refund the credit if it was deducted
            if user_credit.credits_remaining < UserCredit.objects.get(user=request.user).credits_remaining:
                user_credit.credits_remaining += 1
                user_credit.save()

            return Response(
                {'error': f'Failed to generate AI suggestions: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserCreditView(generics.RetrieveAPIView):
    """API view to get user credit information"""
    serializer_class = UserCreditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the user's credit object"""
        return UserCredit.objects.get(user=self.request.user)
