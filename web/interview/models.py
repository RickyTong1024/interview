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
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=32)
    difficulty = models.ForeignKey(difficulty_model, on_delete=models.CASCADE)
    tags = models.ManyToManyField(tag_model)
    languages = models.ManyToManyField(language_model)
    can_exam = models.BooleanField(default=False)
    submission_number = models.BigIntegerField(default=0)
    accepted_number = models.BigIntegerField(default=0)

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save(update_fields=["submission_number"])

    def add_ac_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save(update_fields=["accepted_number"])
	
    class Meta:
        db_table = "interview_problem"

class submission_model(models.Model):
    user_id = models.IntegerField()
    problem_id = models.IntegerField()
    examination_sub_id = models.IntegerField()
    language = models.CharField(max_length=64)
    code = models.TextField()
    state = models.IntegerField(default=0)
    res = models.IntegerField(default=0)
    cpu = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "interview_submission"

class examination_sub_model(models.Model):
    problem_id = models.IntegerField()
    examination_id = models.IntegerField()
    submissions = models.ManyToManyField(submission_model)
    result = models.IntegerField(default=-1)
    submission_number = models.BigIntegerField(default=0)

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save(update_fields=["submission_number"])

    class Meta:
        db_table = "interview_examination_sub"

class examination_model(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    duration = models.IntegerField(default=120)
    subs = models.ManyToManyField(tag_model)

    class Meta:
        db_table = "interview_examination"
