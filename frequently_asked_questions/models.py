from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)  # Field to store the FAQ question
    answer = models.TextField()  # Field to store the FAQ answer
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the FAQ was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the FAQ was last updated

    class Meta:
        verbose_name = "Frequently Asked Question"  # Singular name for the model
        verbose_name_plural = "Frequently Asked Questions"  # Plural name for the model
        ordering = ['created_at']  # Default ordering of the FAQs

    def __str__(self):
        return self.question  # String representation of the model
