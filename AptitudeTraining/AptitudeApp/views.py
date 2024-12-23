from django.shortcuts import render,HttpResponse
from django.http import HttpResponse
from .models import *

# Create your views here.
def home(request):
    return render(request,"public/index.html")

def login(request):
    if 'submit' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if Login.objects.filter(username=username,password=password).exists():
            res = Login.objects.get(username=username,password=password)
            request.session['login_id']=res.pk
            login_id=request.session['login_id']

            if res.user_type =='admin':
                request.session['log']="in"
                return HttpResponse(f"<script>alert('welcome Admin');window.location='adminhome'</script>")
        else:
            return HttpResponse(f"<script>alert('invalid username or password');window.location=''</script>")
    return render(request,'public/login.html')

def changepassword(request):
    if 'submit' in request.POST: 
        current_password = request.POST['current']
        new_password = request.POST['new']
        confirm_new_password = request.POST['cnew']
        data=Login.objects.get(id=request.session['login_id'])
        if data.password==current_password :
            if new_password==confirm_new_password:
                data.password=new_password
                data.save()
                return HttpResponse(f"<script>alert('Password changed successfully');window.location='/adminhome'</script>")
            else:
                return HttpResponse(f"<script>alert('Confirm password does not matches');window.location='/changepassword'</script>")
        else:
            return HttpResponse(f"<script>alert('Current password is incorrect');window.location='/changepassword'</script>")
    return render(request,'admin/changepassword.html')

def signup(request):
    return render(request,"public/signup.html")

def adminhome(request):
    return render(request,"admin/adminhome.html")

#Manage Education Contents
def addeducontent(request):
    if 'submit' in request.POST:
        title=request.POST['title']
        description=request.POST['description']
        type=request.POST['type']
        content=request.POST['content']
        q=Education_Content(title=title,description=description,file_type=type,file_path=content)
        q.save()
        return HttpResponse(f"<script>alert('Content added successfully');window.location='/vieweducontent'</script>")
    return render(request,"admin/addeducontent.html")

def vieweducontent(request):
    data=Education_Content.objects.all()
    return render(request,"admin/vieweducontent.html",{'data':data})

def updateeducontent(request,id):
    data=Education_Content.objects.get(id=id)
    if 'submit' in request.POST:
        title=request.POST['title']
        description=request.POST['description']
        type=request.POST['type']
        content=request.POST['content']

        data.title=title
        data.description=description
        data.file_path=content
        data.file_type=type
        data.save()
        return HttpResponse(f"<script>alert('Content updated successfully');window.location='/vieweducontent'</script>")
    return render(request,"admin/updateeducontent.html",{'data':data})

def deleteeducontent(request,id):
    data=Education_Content.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert('Content deleted successfully');window.location='/vieweducontent'</script>")
    
#Manage Questions
def addquestion(request):
    if 'submit' in request.POST:
        question=request.POST['question']
        optiona=request.POST['optiona']
        optionb=request.POST['optionb']
        optionc=request.POST['optionc']
        optiond=request.POST['optiond']
        type=request.POST['type']
        answer=request.POST['answer']
        description=request.POST['description']
        difficulty=request.POST['difficulty']
        q=Questions(question=question,optiona=optiona,optionb=optionb,optionc=optionc,optiond=optiond,question_type=type,answer_description=description,question_level=difficulty,answer=answer)
        q.save()
        return HttpResponse(f"<script>alert('Content added successfully');window.location='/viewquestions'</script>")
    return render(request,"admin/addquestion.html")

def viewquestions(request):
    data=Questions.objects.all()
    return render(request,"admin/viewquestions.html",{'data':data})

def updatequestion(request,id):
    data=Questions.objects.get(id=id)
    if 'submit' in request.POST:
        question=request.POST['question']
        optiona=request.POST['optiona']
        optionb=request.POST['optionb']
        optionc=request.POST['optionc']
        optiond=request.POST['optiond']
        typeqn=request.POST['type']
        answer=request.POST['answer']
        description=request.POST['description']
        difficulty=request.POST['difficulty']

        data.question=question
        data.optiona=optiona
        data.optionb=optionb
        data.optionc=optionc
        data.optiond=optiond
        data.question_type=typeqn
        data.answer=answer
        data.answer_description=description
        data.question_level=difficulty
        data.save()
        return HttpResponse(f"<script>alert('Content updated successfully');window.location='/viewquestions'</script>")
    return render(request,"admin/updatequestion.html",{'data':data})

def deletequestion(request,id):
    data=Questions.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert('Content deleted successfully');window.location='/viewquestions'</script>")

#Feedback
def viewfeedbacks(request):
    data=Feedback.objects.all()
    return render(request,"admin/viewfeedbacks.html",{'data':data})

#Complaints
def viewcomplaints(request):
    data=Complaint.objects.all()
    return render(request,"admin/viewcomplaints.html",{'data':data})

def sentreply(request,id):
    data=Complaint.objects.get(id=id)
    if 'submit' in request.POST:
        reply=request.POST['reply']
        data.complaint_reply=reply
        data.complaint_status="YES"
        data.save()
        return HttpResponse(f"<script>alert('Reply Sent Successfully');window.location='/viewcomplaints'</script>")
    return render(request,"admin/sentreply.html",{'data':data})

def index1(request):
    return render(request,"index1.html")
# def userchangepassword(request):
#     return render(request,"user/changepassword.html")

# def feedback(request):
#     return render(request,"user/feedback.html")