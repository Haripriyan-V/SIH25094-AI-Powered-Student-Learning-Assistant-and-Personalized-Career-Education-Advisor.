from django.conf import settings
from django.db import models
from students.models import Skill, Interest


class CareerField(models.Model):
    """Broad domain e.g. Technology, Healthcare, Commerce."""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CareerPath(models.Model):
    """A specific career/job role students can be matched towards."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    career_field = models.ForeignKey(CareerField, on_delete=models.CASCADE, related_name='career_paths')
    required_skills = models.ManyToManyField(Skill, blank=True, related_name='career_paths')
    related_interests = models.ManyToManyField(Interest, blank=True, related_name='career_paths')
    average_salary_lpa = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True,
        help_text="Average annual salary in Lakhs Per Annum (India)"
    )
    growth_outlook = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High'), ('very_high', 'Very High')],
        default='moderate',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class AssessmentTest(models.Model):
    """A career-aptitude / psychometric assessment containing multiple questions."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AssessmentQuestion(models.Model):
    test = models.ForeignKey(AssessmentTest, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    # The career field this question is designed to score affinity towards.
    related_career_field = models.ForeignKey(
        CareerField, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessment_questions'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Q: {self.text[:50]}"


class AssessmentOption(models.Model):
    question = models.ForeignKey(AssessmentQuestion, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    score_weight = models.IntegerField(default=1, help_text="Weight added to the related career field's score if chosen.")

    def __str__(self):
        return self.text


class AssessmentResult(models.Model):
    """Stores a student's completed attempt at an AssessmentTest, with computed field scores."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_results')
    test = models.ForeignKey(AssessmentTest, on_delete=models.CASCADE, related_name='results')
    field_scores = models.JSONField(default=dict, help_text="{career_field_id: score} mapping computed from answers")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.student.username} - {self.test.title}"


class CareerRecommendation(models.Model):
    """
    AI-generated (or rule-based) career suggestion for a student, with a
    match score and short reasoning text that the recommendation engine
    (Phase 3 - AI module) can populate.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='career_recommendations')
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='recommendations')
    match_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="0-100 compatibility score")
    reasoning = models.TextField(blank=True, null=True, help_text="AI-generated explanation for this recommendation")
    source_assessment = models.ForeignKey(
        AssessmentResult, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommendations'
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-match_score']
        unique_together = ('student', 'career_path', 'source_assessment')

    def __str__(self):
        return f"{self.student.username} -> {self.career_path.title} ({self.match_score}%)"
