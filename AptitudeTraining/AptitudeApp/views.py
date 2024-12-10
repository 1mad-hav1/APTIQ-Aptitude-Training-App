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
            return HttpResponse(f"<script>alert('invalid username or password');window.location='login'</script>")
    return render(request,'public/login.html')



    return render(request,"public/login.html")

def signup(request):
    return render(request,"public/signup.html")

def adminchangepassword(request):
    return render(request,"admin/changepassword.html")

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
    return HttpResponse(f"<script>alert('Content updated successfully');window.location='/vieweducontent'</script>")
    
def addquestion(request):
    if 'submit' in request.POST:
        question=request.POST['question']
        optiona=request.POST['optiona']
        optionb=request.POST['optionb']
        optionc=request.POST['optionc']
        optiond=request.POST['optiond']
        typeqn=request.POST['typeqn']
        answer=request.POST['answer']
        difficulty=request.POST['difficulty']
        q=Questions(question=question,optiona=optiona,optionb=optionb,optionc=optionc,optiond=optiond,question_type=typeqn,answer_description=difficulty,answer=answer)
        q.save()
        return HttpResponse(f"<script>alert('Content added successfully');window.location='/vieweducontent'</script>")
    return render(request,"admin/addquestion.html")

def viewquestion(request):
    data=Questions.objects.all()
    return render(request,"admin/viewquestion.html",{'data':data})

def adminhome(request):
    return render(request,"admin/adminhome.html")

def userchangepassword(request):
    return render(request,"user/changepassword.html")

def feedback(request):
    return render(request,"user/feedback.html")