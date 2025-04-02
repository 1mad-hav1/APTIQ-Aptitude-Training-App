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
    progress=models.CharField(max_length=50,default='0')
    user_level=models.CharField(max_length=50,default='Beginner')

class Education_Content(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=5000)
    content_type=models.CharField(max_length=50)
    difficulty=models.CharField(max_length=50)

class Section_Test(models.Model):
    EDUCATION_CONTENT=models.ForeignKey(Education_Content,on_delete=models.CASCADE)
    question=models.CharField(max_length=5000)
    optiona=models.CharField(max_length=500)
    optionb=models.CharField(max_length=500)
    optionc=models.CharField(max_length=500)
    optiond=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    
class User_Educontent_Complete(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    EDUCATION_CONTENT=models.ForeignKey(Education_Content,on_delete=models.CASCADE)
    completed=models.CharField(max_length=500,default="No")
    
class Video_Content(models.Model):
    link=models.CharField(max_length=50)
    EDUCATION_CONTENT=models.ForeignKey(Education_Content,on_delete=models.CASCADE)

class Questions(models.Model):
    question=models.CharField(max_length=5000)
    optiona=models.CharField(max_length=500)
    optionb=models.CharField(max_length=500)
    optionc=models.CharField(max_length=500)
    optiond=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    question_type=models.CharField(max_length=50)
    difficulty=models.CharField(max_length=50)
    answer_description=models.CharField(max_length=5000)
    
class Test(models.Model):
    test_name=models.CharField(max_length=50)
    test_date=models.CharField(max_length=50)
    test_difficulty=models.CharField(max_length=50)
    test_num_of_qns=models.CharField(max_length=50)
    test_num_of_qns_logical=models.CharField(max_length=50)
    test_num_of_qns_quantitative=models.CharField(max_length=50)
    test_num_of_qns_verbal=models.CharField(max_length=50)
    test_time=models.CharField(max_length=50)
    test_topics=models.CharField(max_length=50)
    test_passmark=models.CharField(max_length=50)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    cp=models.CharField(max_length=50,default='0')

class Test_Question(models.Model):
    TEST=models.ForeignKey(Test,on_delete=models.CASCADE)
    QUESTIONS=models.ForeignKey(Questions,on_delete=models.CASCADE)

class Result(models.Model):
    TEST=models.ForeignKey(Test,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    mark_scored=models.CharField(max_length=50)
    logical_score = models.CharField(max_length=50)
    verbal_score = models.CharField(max_length=50)
    quant_score = models.CharField(max_length=50)
    pass_fail=models.CharField(max_length=50)


class Complaint(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint_description=models.CharField(max_length=500)
    complaint_date=models.CharField(max_length=50)
    complaint_reply=models.CharField(max_length=500,null=True)
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


class TempQuestions(models.Model):
    question=models.CharField(max_length=5000)
    optiona=models.CharField(max_length=500)
    optionb=models.CharField(max_length=500)
    optionc=models.CharField(max_length=500)
    optiond=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    question_type=models.CharField(max_length=50)
    difficulty=models.CharField(max_length=50)
    answer_description=models.CharField(max_length=5000)
    
class performance(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    accuracy=models.CharField(max_length=500)
    improvment_rate=models.CharField(max_length=500)
    difficulty_score=models.CharField(max_length=500)
    date=models.CharField(max_length=50)

class CareerPrediction(models.Model):
    job_role=models.CharField(max_length=500)
    job_description=models.CharField(max_length=5000)

class CompanyQuestions(models.Model):
    question=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    answer_description=models.CharField(max_length=500)
    company_name=models.CharField(max_length=500)
