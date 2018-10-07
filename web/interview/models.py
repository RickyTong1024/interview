from django.db import models

class difficulty_model(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
        
    class Meta:
        db_table = "interview_difficulty"

class tag_model(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
	
    class Meta:
        db_table = "interview_tag"

class language_model(models.Model):
    name = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)

    def __str__(self):
        return self.name
	
    class Meta:
        db_table = "interview_language"
	
class problem_model(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    difficulty = models.ForeignKey(difficulty_model, on_delete=models.CASCADE)
    tags = models.ManyToManyField(tag_model)
    languages = models.ManyToManyField(language_model)
    test_case_info = models.TextField()
	
    class Meta:
        db_table = "interview_problem"
