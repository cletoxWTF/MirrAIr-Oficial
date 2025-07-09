from django.db import models

class BenchmarkResult(models.Model):
    input_text = models.TextField()
    chatgpt_response = models.TextField()
    deepseek_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    metrics = models.JSONField(default=dict)

    class Meta:
        db_table = 'benchmark_results'
