from django.db import models

class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    user_type=models.CharField(max_length=50)

class User(models.Model):
    LOGIN=models.ForeignKey(Login, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    dob=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    photo=models.CharField(max_length=50)

class Education_Content(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    file_type=models.CharField(max_length=50)
    file_path=models.CharField(max_length=50)

class Questions(models.Model):
    question=models.CharField(max_length=50)
    optiona=models.CharField(max_length=50)
    optionb=models.CharField(max_length=50)
    optionc=models.CharField(max_length=50)
    optiond=models.CharField(max_length=50)
    answer=models.CharField(max_length=50)
    question_type=models.CharField(max_length=50)
    question_level=models.CharField(max_length=50)
    answer_description=models.CharField(max_length=500)
    
class Test(models.Model):
    test_name=models.CharField(max_length=50)
    test_date=models.CharField(max_length=50)
    test_description=models.CharField(max_length=500)
    test_status=models.CharField(max_length=50)
    
class Test_Question(models.Model):
    TEST=models.ForeignKey(Test,on_delete=models.CASCADE)
    QUESTIONS=models.ForeignKey(Questions,on_delete=models.CASCADE)

class Result(models.Model):
    TESTQUESTION=models.ForeignKey(Test_Question,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    passmark=models.CharField(max_length=50,null=True)
    mark=models.CharField(max_length=50)
    pass_fail=models.CharField(max_length=50)
    result_date=models.CharField(max_length=50)

class Complaint(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint_description=models.CharField(max_length=500)
    complaint_date=models.CharField(max_length=50)
    complaint_reply=models.CharField(max_length=500)
    complaint_status=models.CharField(max_length=50)

class Feedback(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    feedback_description=models.CharField(max_length=500)
    feedback_date=models.CharField(max_length=50)

class Prediction_Result(models.Model):
    quantitative_aptitude_score=models.CharField(max_length=50)
    logical_aptitude_score=models.CharField(max_length=50)
    verbal_aptitude_score=models.CharField(max_length=50)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    prediction_result=models.CharField(max_length=500)


