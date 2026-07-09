from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
    duration_hours = models.PositiveIntegerField(default=1)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_created'
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class LearningResource(models.Model):
    class ResourceType(models.TextChoices):
        VIDEO = 'video', 'Video'
        ARTICLE = 'article', 'Article'
        PDF = 'pdf', 'PDF'
        LINK = 'link', 'External Link'

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices, default=ResourceType.ARTICLE)
    url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='learning_resources/', blank=True, null=True)
    content = models.TextField(blank=True, null=True, help_text="Inline text content for article-type resources.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    passing_score = models.PositiveIntegerField(default=50, help_text="Passing percentage")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Q: {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'correct' if self.is_correct else 'incorrect'})"


class QuizAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.score}%)"


class StudentProgress(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_progress')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    progress_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-last_accessed']

    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.progress_percent}%)"


# ---------------------------------------------------------------------------
# Scholarship
# ---------------------------------------------------------------------------

class Scholarship(models.Model):
    """A scholarship opportunity students can apply for."""

    class ScholarshipType(models.TextChoices):
        MERIT = 'merit', 'Merit Based'
        NEED = 'need', 'Need Based'
        SPORTS = 'sports', 'Sports'
        MINORITY = 'minority', 'Minority'
        GOVERNMENT = 'government', 'Government'
        PRIVATE = 'private', 'Private'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, help_text="Organisation or government body offering the scholarship")
    description = models.TextField()
    scholarship_type = models.CharField(
        max_length=20, choices=ScholarshipType.choices, default=ScholarshipType.MERIT
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True,
        help_text="Annual scholarship amount in INR"
    )
    eligibility = models.TextField(blank=True, null=True, help_text="Eligibility criteria")
    deadline = models.DateField(blank=True, null=True, help_text="Application deadline")
    application_url = models.URLField(blank=True, null=True, help_text="Link to apply")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# College
# ---------------------------------------------------------------------------

class College(models.Model):
    """A college / university that students can explore."""

    class CollegeType(models.TextChoices):
        IIT = 'iit', 'IIT'
        NIT = 'nit', 'NIT'
        IIIT = 'iiit', 'IIIT'
        CENTRAL = 'central', 'Central University'
        STATE = 'state', 'State University'
        DEEMED = 'deemed', 'Deemed University'
        PRIVATE = 'private', 'Private'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True, help_text="City, State")
    college_type = models.CharField(
        max_length=20, choices=CollegeType.choices, default=CollegeType.OTHER
    )
    affiliation = models.CharField(
        max_length=255, blank=True, null=True, help_text="Affiliated board / university"
    )
    ranking = models.PositiveIntegerField(
        blank=True, null=True, help_text="NIRF or equivalent national rank"
    )
    website = models.URLField(blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ranking', 'name']

    def __str__(self):
        return self.name
