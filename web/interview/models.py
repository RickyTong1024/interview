from django.db import models
from django.contrib.auth.models import User as user_model
import datetime

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
    memory_limit = models.IntegerField(default=128)
    difficulty = models.ForeignKey(difficulty_model, on_delete=models.CASCADE, default=1)
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
    examination_id = models.IntegerField()
    language = models.CharField(max_length=64)
    code = models.TextField()
    state = models.IntegerField(default=0)
    res = models.IntegerField(default=0)
    cpu = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    def get_problem(self):
        return problem_model.objects.filter(id=self.problem_id).first()

    def get_user(self):
        return user_model.objects.filter(id=self.user_id).first()

    def get_memory(self):
        return int(self.memory / 1024)

    class Meta:
        db_table = "interview_submission"

class examination_sub_model(models.Model):
    problem_id = models.IntegerField()
    examination_id = models.IntegerField()
    submissions = models.ManyToManyField(submission_model)
    result = models.IntegerField(default=-1)

    def get_problem(self):
        return problem_model.objects.filter(id=self.problem_id).first()

    def get_total_submission(self):
        return len(self.submissions.all())

    class Meta:
        db_table = "interview_examination_sub"

class examination_model(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    duration = models.IntegerField(default=180)
    subs = models.ManyToManyField(examination_sub_model)

    def get_state(self):
        if self.start_time > datetime.datetime.now():
            return 0
        elif  datetime.timedelta(minutes=self.duration) > datetime.datetime.now() - self.start_time:
            return 1
        return 2

    def get_remain_time(self):
        d = self.start_time + datetime.timedelta(minutes=self.duration) - datetime.datetime.now()
        return int(d.total_seconds())
    
    def get_user(self):
        return user_model.objects.filter(id=self.user_id).first()

    def get_total(self):
        return len(self.subs.all())

    def get_accept(self):
        ac = 0
        for sub in self.subs.all():
            examination_sub = examination_sub_model.objects.filter(id=sub.id).first()
            if examination_sub and examination_sub.result == 0:
                ac = ac + 1
        return ac

    def get_score(self):
        if self.get_total() == 0:
            return 0
        return int(self.get_accept() * 100 / self.get_total())

    class Meta:
        db_table = "interview_examination"
