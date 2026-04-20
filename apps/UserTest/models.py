from django.db import models
from django.contrib.auth import get_user_model

from apps.TestCase.models import TestAnswer,TestCase

User = get_user_model()


class Exam(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="exams"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f"Exam {self.id} - User {self.user_id}"
    
class ExamTestCase(models.Model):
    
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="exam_test_cases"
    )

    test_case = models.ForeignKey(
        TestCase,
        on_delete=models.CASCADE,
        related_name="exam_links"
    )

    selected_answer = models.ForeignKey(
        TestAnswer,
        on_delete=models.CASCADE,
        related_name="selected_in_exams",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "exam_test_case"
        unique_together = ("exam", "test_case")
        indexes = [
            models.Index(fields=["exam"]),
            models.Index(fields=["test_case"]),
        ]

    def __str__(self):
        return f"Exam {self.exam_id} - TestCase {self.test_case_id}"