from rest_framework import serializers
from students.serializers import SkillSerializer, InterestSerializer
from .models import (
    CareerField, CareerPath, AssessmentTest, AssessmentQuestion,
    AssessmentOption, AssessmentResult, CareerRecommendation,
)


class CareerFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerField
        fields = ('id', 'name', 'description')


class CareerPathSerializer(serializers.ModelSerializer):
    career_field_name = serializers.CharField(source='career_field.name', read_only=True)
    required_skills = SkillSerializer(many=True, read_only=True)
    related_interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = CareerPath
        fields = (
            'id', 'title', 'description', 'career_field', 'career_field_name',
            'required_skills', 'related_interests', 'average_salary_lpa',
            'growth_outlook', 'created_at',
        )


class CareerPathListSerializer(serializers.ModelSerializer):
    career_field_name = serializers.CharField(source='career_field.name', read_only=True)

    class Meta:
        model = CareerPath
        fields = ('id', 'title', 'career_field', 'career_field_name', 'average_salary_lpa', 'growth_outlook')


class AssessmentOptionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentOption
        fields = ('id', 'text')  # score_weight hidden from students


class AssessmentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentOption
        fields = ('id', 'question', 'text', 'score_weight')


class AssessmentQuestionPublicSerializer(serializers.ModelSerializer):
    options = AssessmentOptionPublicSerializer(many=True, read_only=True)

    class Meta:
        model = AssessmentQuestion
        fields = ('id', 'text', 'order', 'options')


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    options = AssessmentOptionSerializer(many=True, read_only=True)

    class Meta:
        model = AssessmentQuestion
        fields = ('id', 'test', 'text', 'related_career_field', 'order', 'options')


class AssessmentTestPublicSerializer(serializers.ModelSerializer):
    questions = AssessmentQuestionPublicSerializer(many=True, read_only=True)

    class Meta:
        model = AssessmentTest
        fields = ('id', 'title', 'description', 'is_active', 'questions')


class AssessmentTestSerializer(serializers.ModelSerializer):
    questions = AssessmentQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = AssessmentTest
        fields = ('id', 'title', 'description', 'is_active', 'questions', 'created_at')


class AssessmentSubmissionSerializer(serializers.Serializer):
    """Payload: {"answers": {"<question_id>": <option_id>, ...}}"""
    answers = serializers.DictField(child=serializers.IntegerField())


class AssessmentResultSerializer(serializers.ModelSerializer):
    test_title = serializers.CharField(source='test.title', read_only=True)

    class Meta:
        model = AssessmentResult
        fields = ('id', 'student', 'test', 'test_title', 'field_scores', 'completed_at')
        read_only_fields = ('student', 'field_scores', 'completed_at')


class CareerRecommendationSerializer(serializers.ModelSerializer):
    career_path_detail = CareerPathListSerializer(source='career_path', read_only=True)

    class Meta:
        model = CareerRecommendation
        fields = (
            'id', 'student', 'career_path', 'career_path_detail', 'match_score',
            'reasoning', 'source_assessment', 'generated_at',
        )
        read_only_fields = ('student', 'generated_at')
