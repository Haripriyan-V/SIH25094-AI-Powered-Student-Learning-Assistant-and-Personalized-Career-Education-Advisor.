from rest_framework import serializers
from .models import (
    Subject, Course, LearningResource, Quiz, Question, Choice,
    QuizAttempt, StudentProgress, Scholarship, College,
)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description')


class LearningResourceSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = LearningResource
        fields = ('id', 'course', 'course_title', 'title', 'resource_type', 'url', 'file', 'content', 'order')
        read_only_fields = ('id',)


class CourseSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    resources = LearningResourceSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Course
        fields = (
            'id', 'title', 'description', 'subject', 'subject_name', 'level',
            'duration_hours', 'thumbnail', 'created_by', 'created_by_username',
            'is_published', 'resources', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_by', 'created_at', 'updated_at')


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for course list views (no nested resources)."""
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Course
        fields = (
            'id', 'title', 'description', 'subject', 'subject_name',
            'level', 'duration_hours', 'thumbnail', 'is_published', 'created_at',
        )


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text', 'is_correct')


class ChoicePublicSerializer(serializers.ModelSerializer):
    """Hides `is_correct` so students can't see answers before submitting."""
    class Meta:
        model = Choice
        fields = ('id', 'text')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'quiz', 'text', 'order', 'choices')


class QuestionPublicSerializer(serializers.ModelSerializer):
    choices = ChoicePublicSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'order', 'choices')


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'course', 'title', 'description', 'passing_score', 'questions', 'created_at')


class QuizPublicSerializer(serializers.ModelSerializer):
    """Used when a student is about to attempt the quiz (answers hidden)."""
    questions = QuestionPublicSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'course', 'title', 'description', 'passing_score', 'questions')


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ('id', 'student', 'quiz', 'quiz_title', 'score', 'passed', 'started_at', 'completed_at')
        read_only_fields = ('student', 'score', 'passed', 'started_at', 'completed_at')


class QuizSubmissionSerializer(serializers.Serializer):
    """Payload for submitting answers: {"answers": {"<question_id>": <choice_id>, ...}}"""
    answers = serializers.DictField(child=serializers.IntegerField())


class StudentProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = StudentProgress
        fields = ('id', 'student', 'course', 'course_title', 'status', 'progress_percent', 'last_accessed')
        read_only_fields = ('student', 'last_accessed')


# ---------------------------------------------------------------------------
# Scholarship serializers
# ---------------------------------------------------------------------------

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = (
            'id', 'name', 'provider', 'description', 'scholarship_type',
            'amount', 'eligibility', 'deadline', 'application_url',
            'is_active', 'created_at',
        )


# ---------------------------------------------------------------------------
# College serializers
# ---------------------------------------------------------------------------

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = (
            'id', 'name', 'location', 'college_type', 'affiliation',
            'ranking', 'website', 'established_year', 'description',
            'is_active', 'created_at',
        )
