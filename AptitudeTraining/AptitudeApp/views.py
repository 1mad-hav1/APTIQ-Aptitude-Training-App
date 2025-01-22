import base64
import time
import random

from django.shortcuts import render,HttpResponse
from django.http import HttpResponse, JsonResponse
from .models import *

from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

# Create your views here.
def home(request):
    return render(request,"public/index.html")

def admin_learn_more(request):
    return render(request, './admin/adminlearnmore.html')

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

def logout(request):
    request.session['log']="out"
    return HttpResponse(f"<script>alert('Logged Out');window.location='/'</script>")

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
    if request.method == "POST" and 'submit' in request.POST:
        # Save the main educational content
        title = request.POST['title']
        description = request.POST['description']
        description = description.replace('→', '->')
        content_type = request.POST['type']
        difficulty = request.POST['difficulty']
        q = Education_Content.objects.create(
            title=title, description=description, content_type=content_type, difficulty=difficulty)

        # Save the video links
        video_links = request.POST.getlist('video_links[]')  # Get all submitted video links
        for link in video_links:
            if link.strip():  # Avoid saving empty links
                Video_Content.objects.create(
                    EDUCATION_CONTENT_id=q.pk,  # Foreign key to the created content
                    link=link.strip())
        return HttpResponse(f"<script>alert('Content added successfully');window.location='/vieweducontent'</script>")
    return render(request,"admin/addeducontent.html")

def vieweducontent(request):
    # Fetch all the content
    data = Education_Content.objects.all()

    # Sort the data first by content_type, then by difficulty
    sorted_data = {}
    for content in data:
        # Group by content_type
        if content.content_type not in sorted_data:
            sorted_data[content.content_type] = []

        # Add the content to the corresponding content_type group
        sorted_data[content.content_type].append(content)

    # Now, sort each content_type group by difficulty ("easy" < "medium" < "hard")
    difficulty_order = ["Easy", "Medium", "Hard"]

    for content_type, contents in sorted_data.items():
        sorted_data[content_type] = sorted(contents, key=lambda x: difficulty_order.index(x.difficulty))

    return render(request, "admin/vieweducontent.html", {'sorted_data': sorted_data})

def get_video_links(request, id):
    video_data = Video_Content.objects.filter(EDUCATION_CONTENT_id=id)
    if video_data.exists():
        links = [{"id": video.id, "link": video.link} for video in video_data]
    else:
        links = []  # No video links available

    return JsonResponse({"video_links": links})

def updateeducontent(request, id):
    data = Education_Content.objects.get(id=id)
    video_data = Video_Content.objects.filter(EDUCATION_CONTENT_id=id)

    if 'submit' in request.POST:
        # Update basic fields
        title = request.POST['title']
        description = request.POST['description']
        content_type = request.POST['type']
        difficulty = request.POST['difficulty']

        data.title = title
        data.description = description
        data.content_type = content_type
        data.difficulty = difficulty
        data.save()

        # Update existing video links
        existing_video_links = request.POST.dict()  # Convert POST to dictionary for key-value access
        for video in video_data:
            video_link_key = f'existing_video_links[{video.id}]'  # Construct the key dynamically
            if video_link_key in existing_video_links:
                video.link = existing_video_links[video_link_key]
                video.save()

        # Delete removed video links
        existing_video_ids = set(video_data.values_list('id', flat=True))
        posted_video_ids = set(
            int(key.split('[')[1].split(']')[0])  # Extract video ID from key
            for key in existing_video_links.keys()
            if key.startswith('existing_video_links[')
        )
        deleted_video_ids = existing_video_ids - posted_video_ids
        Video_Content.objects.filter(id__in=deleted_video_ids).delete()

        # Add new video links
        new_links = request.POST.getlist('new_video_links[]')
        for new_link in new_links:
            if new_link.strip():  # Avoid empty links
                Video_Content.objects.create(
                    EDUCATION_CONTENT_id=data.pk,
                    link=new_link
                )

        return HttpResponse(
            "<script>alert('Content updated successfully');"
            "window.location='/vieweducontent'</script>"
        )

    return render(request, "admin/updateeducontent.html", {'data': data, 'video_data': video_data})


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
        q=Questions(question=question,optiona=optiona,optionb=optionb,optionc=optionc,optiond=optiond,question_type=type,answer_description=description,difficulty=difficulty,answer=answer)
        q.save()
        return HttpResponse(f"<script>alert('Content added successfully');window.location='/viewquestions'</script>")
    return render(request,"admin/addquestion.html")

def viewquestions(request):
    data=Questions.objects.all()
    # Sort the data first by content_type, then by difficulty
    sorted_data = {}
    for content in data:
        # Group by content_type
        if content.question_type not in sorted_data:
            sorted_data[content.question_type] = []

        # Add the content to the corresponding content_type group
        sorted_data[content.question_type].append(content)

    # Now, sort each content_type group by difficulty ("easy" < "medium" < "hard")
    difficulty_order = ["Easy", "Medium", "Hard"]

    for content_type, contents in sorted_data.items():
        sorted_data[content_type] = sorted(contents, key=lambda x: difficulty_order.index(x.difficulty))
    return render(request,"admin/viewquestions.html",{'sorted_data': sorted_data})

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
        data.difficulty=difficulty
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

#Android
#User App

def and_user_registration(request):
    name=request.POST['name']
    email=request.POST['email']
    username=request.POST['username']
    password=request.POST['password']
    place=request.POST['place']
    phone=request.POST['phone']
    gender=request.POST['gender']
    dob=request.POST['dob']
    photo=request.POST['photo']
    profile=base64.b64decode(photo)
    timestr = datetime.now().strftime("%Y%m%d%H%M%S") 
    print(timestr)
    file_name = f"{name}_{timestr}.jpg"
    fs = FileSystemStorage(location='media/')
    fa = fs.save(file_name, ContentFile(profile))
    q=Login(username=username,password=password,user_type='user')
    q.save()
    q1=User(name=name,email=email,phone=phone,gender=gender,dob=dob,photo=f"media/{fa}",place=place,LOGIN_id=q.pk)
    q1.save()
    return JsonResponse({'status':'ok'})

def and_login(request):
    username=request.POST['username']
    password=request.POST['password']
    if Login.objects.filter(username=username,password=password).exists():
        qa=Login.objects.get(username=username,password=password)
        lid=qa.pk
        if qa.user_type=='user':
            try:
                qd=User.objects.get(LOGIN_id=lid)
                uid=qd.pk
                return JsonResponse({'status':'ok','lid':lid,'uid':uid,'user_type':'user'})
            except User.DoesNotExist:
                print('Login Failed.')
                return JsonResponse({'status':'no'})
        else:
            print('Login Failed.')
            return JsonResponse({'status':'no'})
    else:
        print('Login Failed.')
        return JsonResponse({'status':'no'})

def and_sent_feedback(request):
    feedback=request.POST['feedback']
    uid=request.POST['uid']
    print(uid)
    if uid != 'None':
        timestr = time.strftime("%d-%m-%Y")
        print(timestr)
        q=Feedback(feedback_description=feedback,feedback_date=timestr,USER_id=uid)
        q.save()
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'no'})

def and_view_feedbacks(request):
    user_id=request.POST['uid']
    feedbacks=Feedback.objects.filter(USER_id=user_id)
    data=[]
    for i in feedbacks:
        data.append({'feedback':i.feedback_description})
    return JsonResponse({'status':'ok','data':data})

def and_user_profile(request):
    user_id=request.POST['uid']
    user=User.objects.get(id=user_id)
    password=(Login.objects.get(id=user.LOGIN_id)).password
    username=(Login.objects.get(id=user.LOGIN_id)).username
    data=[]
    data.append({'name':user.name,'email':user.email,'username':username,'phone':user.phone,'dob':user.dob,'password':password,'gender':user.gender,'photo':user.photo,'place':user.place})
    return JsonResponse({'status':'ok','data':data})

def and_user_change_password(request):
    current=request.POST['current']
    newpass=request.POST['newpass']
    confirmpass=request.POST['confirmpass']
    lid=request.POST['lid']
    data=Login.objects.get(id=lid)
    if data.password==current :
        if newpass==confirmpass:
            data.password=newpass
            data.save()
            return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'no'})

def and_user_update_profile(request):
    uid=request.POST['uid']
    lid=request.POST['lid']
    userdata=User.objects.get(id=uid)
    logindata=Login.objects.get(id=lid)
    name=request.POST['name']
    userdata.name=name
    userdata.email=request.POST['email']
    logindata.username=request.POST['username']
    userdata.place=request.POST['place']
    userdata.phone=request.POST['phone']
    userdata.gender=request.POST['gender']
    userdata.dob=request.POST['dob']
    if 'photo' in request.POST:
        photo=request.POST['photo']
        profile=base64.b64decode(photo)
        timestr = datetime.now().strftime("%Y%m%d%H%M%S") 
        print(timestr)
        file_name = f"{name}_{timestr}.jpg"
        fs = FileSystemStorage(location='media/')
        fa = fs.save(file_name, ContentFile(profile))
        userdata.photo=f"media/{fa}"
    userdata.save()
    logindata.save()
    return JsonResponse({'status':'ok'})
    
def and_get_study_material(request):
    content_type = request.POST['content_type']
    # Define custom sorting order
    difficulty_order = {'Easy': 1, 'Medium': 2, 'Hard': 3}
    # Filter contents based on content_type
    contents = Education_Content.objects.filter(content_type=content_type)
    # Sort contents using the custom order
    sorted_contents = sorted(
        contents, 
        key=lambda x: difficulty_order.get(x.difficulty, float('inf'))
    )
    data = []
    for i in sorted_contents:
        data.append({'title': i.title, 'id': i.pk, 'difficulty': i.difficulty})
    return JsonResponse({'status': 'ok', 'data': data})

def and_get_detailed_content(request):
    id=request.POST['cid']
    content=Education_Content.objects.get(id=id)
    video_data = Video_Content.objects.filter(EDUCATION_CONTENT_id=id)
    if video_data.exists():
        links = [{"id": video.id, "link": video.link} for video in video_data]
    else:
        links = []
    data = {"id": content.id,"title": content.title,"description": content.description,
                "difficulty": content.difficulty,"content_type": content.content_type}
    return JsonResponse({'status':'ok',"content": data, "video_links": links})

from django.utils.timezone import now
import random

def and_get_test_questions(request):
    difficulty = request.POST.get('difficulty')
    num_qns = int(request.POST.get('num_qns'))
    verbal = request.POST.get('verbal')
    logical = request.POST.get('logical')
    quant = request.POST.get('quant')

    all_questions = list(Questions.objects.all())
    name = request.POST.get('test_name') 
    uid = request.POST.get('uid')
    time = request.POST.get('time')  
    print("hi")
    # Separate questions by type
    verbal_questions = [q for q in all_questions if q.question_type == 'Verbal']
    logical_questions = [q for q in all_questions if q.question_type == 'Logical']
    quant_questions = [q for q in all_questions if q.question_type == 'Quantitative']

    # Separate questions by difficulty
    easy_questions = [q for q in all_questions if q.difficulty == 'Easy']
    medium_questions = [q for q in all_questions if q.difficulty == 'Medium']
    hard_questions = [q for q in all_questions if q.difficulty == 'Hard']

    selected_questions = []

    # Filter by difficulty
    if difficulty == 'Easy':
        selected_questions.extend(random.sample(easy_questions, min(num_qns, len(easy_questions))))
    elif difficulty == 'Medium':
        num_easy = num_qns // 5  # 20% Easy questions
        num_medium = num_qns - num_easy
        selected_questions.extend(random.sample(easy_questions, min(num_easy, len(easy_questions))))
        selected_questions.extend(random.sample(medium_questions, min(num_medium, len(medium_questions))))
    elif difficulty == 'Hard':
        num_easy = num_qns // 10  # 10% Easy questions
        num_medium = num_qns // 5  # 20% Medium questions
        num_hard = num_qns - num_easy - num_medium
        selected_questions.extend(random.sample(easy_questions, min(num_easy, len(easy_questions))))
        selected_questions.extend(random.sample(medium_questions, min(num_medium, len(medium_questions))))
        selected_questions.extend(random.sample(hard_questions, min(num_hard, len(hard_questions))))

    # Apply additional filtering by type
    types_selected = []
    if verbal == '1':
        types_selected.append(verbal_questions)
    if logical == '1':
        types_selected.append(logical_questions)
    if quant == '1':
        types_selected.append(quant_questions)

    if len(types_selected) == 1:
        selected_questions = random.sample(types_selected[0], min(num_qns, len(types_selected[0])))
    elif len(types_selected) == 2:
        type1_count = num_qns // 2
        type2_count = num_qns - type1_count
        selected_questions = random.sample(types_selected[0], min(type1_count, len(types_selected[0]))) + \
                             random.sample(types_selected[1], min(type2_count, len(types_selected[1])))
    elif len(types_selected) == 3:
        type_count = num_qns // 3
        remaining = num_qns - 2 * type_count
        selected_questions = random.sample(types_selected[0], min(type_count, len(types_selected[0]))) + \
                             random.sample(types_selected[1], min(type_count, len(types_selected[1]))) + \
                             random.sample(types_selected[2], min(remaining, len(types_selected[2])))

    # Calculate test pass mark (40% of total questions)
    pass_mark = int(num_qns * 0.4)

    # Create a new Test instance
    test = Test.objects.create(
        test_name=name,
        test_date=now().strftime('%Y-%m-%d %H:%M:%S'),
        test_difficulty=difficulty,
        test_num_of_qns=num_qns,
        test_time=time,
        test_topics=','.join(topic for topic, flag in [('Logical', logical), ('Quantitative', quant), ('Verbal', verbal)] if flag == '1'),
        test_passmark=pass_mark,
        USER_id=uid  
    )

    # Map selected questions to the Test_Question table
    for question in selected_questions:
        Test_Question.objects.create(TEST=test, QUESTIONS=question)

    # Prepare final data
    questions_data = [
        {
            'question': q.question,
            'option1': q.optiona,
            'option2': q.optionb,
            'option3': q.optionc,
            'option4': q.optiond,
            'question_type': q.question_type,
            'correctAnswer': q.answer
        }
        for q in selected_questions
    ]   

    return JsonResponse({'status': 'ok', 'data': questions_data, 'test_id':test.pk})