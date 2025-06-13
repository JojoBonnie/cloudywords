from rest_framework import serializers
from wordcloud_core.models import WordCloud, UserCredit


class WordCloudSerializer(serializers.ModelSerializer):
    """Serializer for WordCloud model"""

    class Meta:
        model = WordCloud
        fields = [
            'id', 'title', 'input_text', 'is_ai_generated',
            'width', 'height', 'font', 'color_scheme', 'background_color',
            'max_words', 'word_density', 'orientation',
            'image_url', 'svg_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'image_url', 'svg_url', 'created_at', 'updated_at']


class WordCloudGenerateSerializer(serializers.Serializer):
    """Serializer for word cloud generation request"""
    title = serializers.CharField(max_length=100)
    input_text = serializers.CharField()
    is_ai_generated = serializers.BooleanField(default=False)
    width = serializers.IntegerField(min_value=100, max_value=2000, default=800)
    height = serializers.IntegerField(min_value=100, max_value=2000, default=400)
    font = serializers.ChoiceField(choices=WordCloud.FONT_CHOICES, default='arial')
    color_scheme = serializers.ChoiceField(choices=WordCloud.COLOR_SCHEME_CHOICES, default='default')
    background_color = serializers.CharField(max_length=20, default='white')
    max_words = serializers.IntegerField(min_value=10, max_value=1000, default=200)
    word_density = serializers.IntegerField(min_value=10, max_value=100, default=80)
    orientation = serializers.ChoiceField(choices=WordCloud.ORIENTATION_CHOICES, default='random')


class WordCloudExportSerializer(serializers.Serializer):
    """Serializer for word cloud export request"""
    format = serializers.ChoiceField(choices=['png', 'svg'])
    resolution = serializers.ChoiceField(choices=['low', 'medium', 'high'], default='medium')


class AIWordSuggestionsSerializer(serializers.Serializer):
    """Serializer for AI word suggestion request"""
    topic = serializers.CharField(max_length=100)
    count = serializers.IntegerField(min_value=10, max_value=500, default=100)


class UserCreditSerializer(serializers.ModelSerializer):
    """Serializer for user credits"""

    class Meta:
        model = UserCredit
        fields = ['credits_remaining', 'last_updated']
        read_only_fields = ['credits_remaining', 'last_updated']
