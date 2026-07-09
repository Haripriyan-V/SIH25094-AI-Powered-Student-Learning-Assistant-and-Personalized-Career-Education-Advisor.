from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import StudentProfile, StudentSkill, Education, Interest, Skill


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id', 'name')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'category')


class StudentSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        source='skill', queryset=Skill.objects.all(), write_only=True
    )

    class Meta:
        model = StudentSkill
        fields = ('id', 'skill_id', 'skill_name', 'proficiency')


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            'id', 'institution_name', 'degree_or_level', 'field_of_study',
            'start_year', 'end_year', 'percentage_or_gpa', 'is_current',
        )

    def validate(self, attrs):
        start = attrs.get('start_year')
        end = attrs.get('end_year')
        if start and end and end < start:
            raise serializers.ValidationError({'end_year': 'End year cannot be before start year.'})
        return attrs


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    interests = InterestSerializer(many=True, read_only=True)
    interest_ids = serializers.PrimaryKeyRelatedField(
        source='interests', queryset=Interest.objects.all(), many=True, write_only=True, required=False
    )
    skills = StudentSkillSerializer(many=True, read_only=True)
    education_history = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = (
            'id', 'user', 'gender', 'grade_or_class', 'school_or_college',
            'bio', 'profile_picture', 'interests', 'interest_ids',
            'skills', 'education_history', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')
