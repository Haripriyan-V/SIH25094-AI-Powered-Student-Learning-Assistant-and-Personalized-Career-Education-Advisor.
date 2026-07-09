from django.conf import settings
from django.db import models


class Interest(models.Model):
    """A topic of interest a student can tag onto their profile (e.g. AI, Design)."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Skill(models.Model):
    """A reusable skill (e.g. Python, Public Speaking) referenced by students and careers."""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    """Extended profile information for a student user."""

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile'
    )
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True)
    grade_or_class = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 10th, 12th, B.Tech 2nd Year")
    school_or_college = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class StudentSkill(models.Model):
    """Through-model linking a student to a skill with a proficiency level."""

    class Proficiency(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='student_skills')
    proficiency = models.CharField(max_length=20, choices=Proficiency.choices, default=Proficiency.BEGINNER)

    class Meta:
        unique_together = ('student_profile', 'skill')

    def __str__(self):
        return f"{self.student_profile.user.username} - {self.skill.name} ({self.proficiency})"


class Education(models.Model):
    """A single academic record (school/college) belonging to a student."""
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='education_history')
    institution_name = models.CharField(max_length=255)
    degree_or_level = models.CharField(max_length=255, help_text="e.g. SSC, HSC, B.Sc Computer Science")
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    percentage_or_gpa = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.institution_name} ({self.degree_or_level})"
