from django.db import models


class TestCase(models.Model):
    question_uz = models.TextField()
    question_uzk = models.TextField()
    question_ru = models.TextField()

    explanation_uz = models.TextField()
    explanation_uzk = models.TextField()
    explanation_ru = models.TextField()

    media = models.FileField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TestCase {self.pk}#"
    

class TestAnswer(models.Model):
    test_case = models.ForeignKey(
        TestCase,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    answer_text_uz = models.TextField(null=True, blank=True)
    answer_text_uzk = models.TextField(null=True, blank=True)
    answer_text_ru = models.TextField(null=True, blank=True)

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer({self.id})"