import base64
import time
import random
import os
from django.shortcuts import render,HttpResponse
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from .models import *
from django.db.models import Min


from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.utils.timezone import now
from AptitudeApp import  question_generation as atst
from itertools import groupby
from operator import itemgetter

import json
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

def add_ai_q(request):
    return render(request,"admin/add_ai_questions.html")
def add_ai_q_post(request):
    category = request.POST['type']
    difficulty = request.POST['difficulty']
    num_questions = request.POST['number']
    TempQuestions.objects.all().delete()
    mcq_questions = atst.generate_mcq(category, difficulty, int(num_questions))
    
    for idx, mcq in enumerate(mcq_questions, 1):
        print(f"\nGenerated MCQ {idx}:")
        
        # Parse the MCQ to extract question, options, correct answer, and explanation
        question, options, correct_answer, explanation = atst.parse_mcq(mcq)
        
        print(f"\n**Original Question:** {question}")
        
        # **Check grammar correctness**
        if not atst.check_grammar(question):
            print(f"Grammar issue detected in: {question}")
            corrected_question = atst.correct_grammar(question)
            print(f"Corrected Question: {corrected_question}")
            question = corrected_question  # Use the corrected version
        
        # **Print Options**
        print("\n**Options:**")
        for key, value in options.items():
            print(f"{key}) {value}")

        # **Validate correct answer before storing**
        if correct_answer != "No answer found" and correct_answer in options:
            print(f"\n**Correct Answer:** {correct_answer}) {options[correct_answer]}")
        else:
            print("\n**Correct Answer:** Not found or invalid answer.")
        
        print(f"\n**Explanation:** {explanation}")

        # **Perform BERT analysis on the question**
        # bert_analysis = atst.analyze_mcq_with_bert(question)
        # print(f"\nBERT Analysis Output for the question '{question}':\n", bert_analysis)

        # **Store data in TempQuestions model**
        optiona = options.get("a", "")
        optionb = options.get("b", "")
        optionc = options.get("c", "")
        optiond = options.get("d", "")

        q = TempQuestions(
            question=question,
            optiona=optiona,
            optionb=optionb,
            optionc=optionc,
            optiond=optiond,
            question_type=category,
            answer_description=explanation,
            difficulty=difficulty,
            answer=correct_answer
        )
        q.save()

    # Fetch all stored questions and render them on the admin page
    dd = TempQuestions.objects.all()
    return render(request, "admin/add_ai_questions.html", {"data": dd})
def temp_all(request):
    dd=TempQuestions.objects.all()
    return render(request,"admin/add_ai_questions.html",{"data":dd})

def deletequestion_temp(request,id):
    data=TempQuestions.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert('Content Deleted successfully');window.location='/temp_all'</script>")

def add_all(request):
    dd=TempQuestions.objects.all()
    for i in dd:
        q=Questions(question=i.question,optiona=i.optiona,optionb=i.optionb,optionc=i.optionc,optiond=i.optionc,question_type=i.question_type,answer_description=i.answer_description,difficulty=i.difficulty,answer=i.answer)
        q.save()
    TempQuestions.objects.all().delete()
    return  HttpResponse(f"<script>alert('Content Added successfully');window.location='/viewquestions'</script>")


def read_pdf(file_path):
    import PyPDF2
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        txt=""
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text = page.extract_text()
            txt=txt+text+" "
        return txt

def careerprediction(request):
    job = request.POST['job']
    ob = Vacancy.objects.filter(vac_name__icontains=job)
    data = []
    for i in ob:
        row = {"cmp": i.COMPANY.company_name, "job": i.JOB.job_name, "vac": i.vac_name, "qual": i.JOB.skills_required, "sal": i.place,
               "det": i.JOB.description, "vid": i.id}
        data.append(row)
    r = json.dumps(data)
    if len(data)>0:
        return JsonResponse({"status":"ok","data":data})
    else:
        return JsonResponse({"status":"no"})
    return HttpResponse(r)

def d(request):

    openness=float(request.POST['openness'])
    conscientiousness=float(request.POST['conscientiousness'])
    extraversion=float(request.POST['extraversion'])
    agreeableness=float(request.POST['agreeableness'])
    neuroticism=float(request.POST['neuroticism'])
    numericalAptitude=float(request.POST['numericalAptitude'])
    spatialAptitude=float(request.POST['spatialAptitude'])
    perceptualAptitude=float(request.POST['perceptualAptitude'])
    abstractReasoning=float(request.POST['abstractReasoning'])
    verbalReasoning=float(request.POST['verbalReasoning'])
    input_features = np.array([[
        float(openness), float(conscientiousness),
        float(extraversion), float(agreeableness),
        float(neuroticism), float(numericalAptitude),
        float(spatialAptitude), float(perceptualAptitude),
        float(abstractReasoning), float(verbalReasoning)
    ]])
    prediction = model.predict(input_features)[0]
    print(prediction)
    if prediction=="Accountant" or prediction=="Salesperson":
        field="Commerce"
    elif prediction=='Graphic Designer' or prediction=='Architect':
        field='Science & Technology'
    elif prediction=='Research Scientist' or prediction=='Environmental Scientist':
        field='Science & Technology'
    elif prediction=='Nurse' or prediction=='Pharmacist':
        field='Medical Science'
    elif prediction=='Journalist' or prediction=='Technical Writer':
        field='Literature'
    elif prediction=='Game Developer'or prediction=='Marketing Analyst':
        field='Science & Technology'
    elif prediction=='Forensic Psychologist' or prediction=='Human Rights Lawyer':
        field='Social Science & Law' 
       
    elif prediction=='Electronics Design Engineer' or prediction=='Robotics Engineer':
        field='Science & Technology'    
    elif prediction=='Insurance Underwriter':
        field='Literature'   
    elif prediction=='Biomedical Researcher':
        field='Medical Science' 
    else:
        field='other'
    if field=="other":
        return JsonResponse({"status":"ok","result":"You can generally choose any area"})
    else:
        return JsonResponse({"status":"ok","result":"Your Predicted area is "+field +". You may choose "+prediction +"in specific"})



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
                user_name=qd.name
                level=qd.user_level
                progress_value=qd.progress
                return JsonResponse({'status':'ok','lid':lid,'uid':uid,'user_level':level,'progress_value':progress_value, 'user_name':user_name,'user_type':'user'})
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
    uid = request.POST['uid']
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
        entry = User_Educontent_Complete.objects.filter(USER_id=uid, EDUCATION_CONTENT_id=i.pk).exists()
        completed = "Yes" if entry else "No"
        data.append({'title': i.title, 'id': i.pk, 'difficulty': i.difficulty, "completed":completed})
    return JsonResponse({'status': 'ok', 'data': data})

def and_get_company_names(request):
    companies = CompanyQuestions.objects.values('company_name').annotate(id=Min('id'))
    data = [{'company_name': company['company_name']} for company in companies]
    print(data)
    return JsonResponse({'status': 'ok', 'data': data}, safe=False)

def and_get_company_questions(request):
    cname = request.POST['cname']

    try:
        company_questions = CompanyQuestions.objects.filter(company_name=cname)
        question_details = []
        for cq in company_questions:
            question_details.append({
                "question": cq.question,
                "correctAnswer": cq.answer,
                "answerDescription": cq.answer_description
            })

        return JsonResponse({"status": "ok", "data": question_details})
    except CompanyQuestions.DoesNotExist:
        return JsonResponse({"status": "error", "message": "No questions found for this company"})

def and_get_detailed_content(request):
    id=request.POST['cid']
    try:
        content=Education_Content.objects.get(id=id)
        video_data = Video_Content.objects.filter(EDUCATION_CONTENT_id=id)
        if video_data.exists():
            links = [{"id": video.id, "link": video.link} for video in video_data]
        else:
            links = []
        data = {"id": content.id,"title": content.title,"description": content.description,
                    "difficulty": content.difficulty,"content_type": content.content_type}
        return JsonResponse({'status':'ok',"content": data, "video_links": links})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

import random
from django.http import JsonResponse
from django.utils.timezone import now

def and_get_test_questionss(request):
    difficulty = request.POST.get('difficulty')
    num_qns = int(request.POST.get('num_qns'))
    verbal = request.POST.get('verbal')
    logical = request.POST.get('logical')
    quant = request.POST.get('quant')
    print(logical,verbal,quant)
    all_questions = list(Questions.objects.all())
    name = request.POST.get('test_name')
    uid = request.POST.get('uid')
    time = request.POST.get('time')

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
    logical_count = 0
    verbal_count = 0
    quant_count = 0
    if verbal == '1' and logical == '1' and quant == '1':
        types_selected.append(verbal_questions)
        verbal_count = num_qns // 3  # Default division
        types_selected.append(logical_questions)
        logical_count = num_qns // 3  # Default division
        types_selected.append(quant_questions)
        quant_count = num_qns - (verbal_count + logical_count)  # Default division
    elif verbal == '1' and logical == '1':
        types_selected.append(verbal_questions)
        verbal_count = num_qns // 2  # Default division
        types_selected.append(logical_questions)
        logical_count = num_qns - verbal_count  # Default division
    elif verbal == '1' and quant == '1':
        types_selected.append(verbal_questions)
        verbal_count = num_qns // 2
        types_selected.append(quant_questions)
        quant_count = num_qns - verbal_count
    elif logical == '1' and quant == '1':
        types_selected.append(logical_questions)
        logical_count = num_qns // 2
        types_selected.append(quant_questions)
        quant_count = num_qns - logical_count
    elif verbal == '1':
        types_selected.append(verbal_questions)
        verbal_count = num_qns
    elif logical == '1':
        types_selected.append(logical_questions)
        logical_count = num_qns
    elif quant == '1':
        types_selected.append(quant_questions)
        quant_count = num_qns
    # Adjust counts for remaining questions based on the selected types
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
        test_num_of_qns_logical=logical_count,
        test_num_of_qns_verbal=verbal_count,
        test_num_of_qns_quantitative=quant_count,
        test_time=time,
        test_topics=','.join(topic for topic, flag in [('Logical', logical), ('Quantitative', quant), ('Verbal', verbal)] if flag == '1'),
        test_passmark=pass_mark,
        USER_id=uid  
    )

    # Map selected questions to the Test_Question table and include IDs
    questions_data = []
    for question in selected_questions:
        Test_Question.objects.create(TEST=test, QUESTIONS=question)
        questions_data.append({
            'id': question.id,  # ID associated within the question data
            'question': question.question,
            'option1': question.optiona,
            'option2': question.optionb,
            'option3': question.optionc,
            'option4': question.optiond,
            'question_type': question.question_type,
            'correctAnswer': question.answer
        })

    return JsonResponse({'status': 'ok', 'data': questions_data, 'test_id': test.pk})


# def and_get_test_questionss(request):
#     difficulty = request.POST.get('difficulty')
#     num_qns = int(request.POST.get('num_qns'))
#     verbal = request.POST.get('verbal')
#     logical = request.POST.get('logical')
#     quant = request.POST.get('quant')

#     all_questions = list(Questions.objects.all())
#     name = request.POST.get('test_name') 
#     uid = request.POST.get('uid')
#     time = request.POST.get('time')  
#     # Separate questions by type
#     verbal_questions = [q for q in all_questions if q.question_type == 'Verbal']
#     logical_questions = [q for q in all_questions if q.question_type == 'Logical']
#     quant_questions = [q for q in all_questions if q.question_type == 'Quantitative']

#     # Separate questions by difficulty
#     easy_questions = [q for q in all_questions if q.difficulty == 'Easy']
#     medium_questions = [q for q in all_questions if q.difficulty == 'Medium']
#     hard_questions = [q for q in all_questions if q.difficulty == 'Hard']

#     selected_questions = []

#     # Filter by difficulty
#     if difficulty == 'Easy':
#         selected_questions.extend(random.sample(easy_questions, min(num_qns, len(easy_questions))))
#     elif difficulty == 'Medium':
#         num_easy = num_qns // 5  # 20% Easy questions
#         num_medium = num_qns - num_easy
#         selected_questions.extend(random.sample(easy_questions, min(num_easy, len(easy_questions))))
#         selected_questions.extend(random.sample(medium_questions, min(num_medium, len(medium_questions))))
#     elif difficulty == 'Hard':
#         num_easy = num_qns // 10  # 10% Easy questions
#         num_medium = num_qns // 5  # 20% Medium questions
#         num_hard = num_qns - num_easy - num_medium
#         selected_questions.extend(random.sample(easy_questions, min(num_easy, len(easy_questions))))
#         selected_questions.extend(random.sample(medium_questions, min(num_medium, len(medium_questions))))
#         selected_questions.extend(random.sample(hard_questions, min(num_hard, len(hard_questions))))

#     # Apply additional filtering by type
#     # Apply additional filtering by type
#     types_selected = []
#     logical_count = 0
#     verbal_count = 0
#     quant_count = 0

#     if verbal == '1':
#         types_selected.append(verbal_questions)
#         verbal_count = num_qns // 3  # Default division
#     if logical == '1':
#         types_selected.append(logical_questions)
#         logical_count = num_qns // 3  # Default division
#     if quant == '1':
#         types_selected.append(quant_questions)
#         quant_count = num_qns // 3  # Default division

#     # Adjust counts for remaining questions based on the selected types
#     if len(types_selected) == 1:
#         if verbal == '1':
#             verbal_count = num_qns
#         elif logical == '1':
#             logical_count = num_qns
#         elif quant == '1':
#             quant_count = num_qns
#         selected_questions = random.sample(types_selected[0], min(num_qns, len(types_selected[0])))

#     elif len(types_selected) == 2:
#         type1_count = num_qns // 2
#         type2_count = num_qns - type1_count
#         selected_questions = random.sample(types_selected[0], min(type1_count, len(types_selected[0]))) + \
#                              random.sample(types_selected[1], min(type2_count, len(types_selected[1])))
#         # Adjust counts based on the type selected
#         if verbal == '1' and logical == '1':
#             verbal_count = type1_count
#             logical_count = type2_count
#         elif verbal == '1' and quant == '1':
#             verbal_count = type1_count
#             quant_count = type2_count
#         elif logical == '1' and quant == '1':
#             logical_count = type1_count
#             quant_count = type2_count

#     elif len(types_selected) == 3:
#         type_count = num_qns // 3
#         remaining = num_qns - 2 * type_count
#         selected_questions = random.sample(types_selected[0], min(type_count, len(types_selected[0]))) + \
#                              random.sample(types_selected[1], min(type_count, len(types_selected[1]))) + \
#                              random.sample(types_selected[2], min(remaining, len(types_selected[2])))
#         verbal_count = type_count
#         logical_count = type_count
#         quant_count = remaining

#     # Calculate test pass mark (40% of total questions)
#     pass_mark = int(num_qns * 0.4)

#     # Create a new Test instance
#     test = Test.objects.create(
#         test_name=name,
#         test_date=now().strftime('%Y-%m-%d %H:%M:%S'),
#         test_difficulty=difficulty,
#         test_num_of_qns=num_qns,
#         test_num_of_qns_logical=logical_count,
#         test_num_of_qns_verbal=verbal_count,
#         test_num_of_qns_quantitative=quant_count,
#         test_time=time,
#         test_topics=','.join(topic for topic, flag in [('Logical', logical), ('Quantitative', quant), ('Verbal', verbal)] if flag == '1'),
#         test_passmark=pass_mark,
#         USER_id=uid  
#     )


#     # Map selected questions to the Test_Question table
#     for question in selected_questions:
#         Test_Question.objects.create(TEST=test, QUESTIONS=question)

#     # Prepare final data
#     questions_data = [
#         {
#             'id': q.id,
#             'question': q.question,
#             'option1': q.optiona,
#             'option2': q.optionb,
#             'option3': q.optionc,
#             'option4': q.optiond,
#             'question_type': q.question_type,
#             'correctAnswer': q.answer
#         }
#         for q in selected_questions
#     ]   
#     print(questions_data)
#     return JsonResponse({'status': 'ok', 'data': questions_data, 'test_id':test.pk})


def and_post_test_resultss(req):
    uid = req.POST["uid"]
    test_id = req.POST["test_id"]
    mark_scored = req.POST["mark_scored"]
    logical_score = req.POST["logical_score"]
    verbal_score = req.POST["verbal_score"]
    quant_score = req.POST["quant_score"]
    pass_fail = req.POST["pass_fail"]
    correct_answer_id = req.POST["correct_answer_ids"]

    # Get the test object
    test = Test.objects.get(id=test_id)

    # Create and save the test result
    result = Result.objects.create(
        TEST_id=test_id,
        USER_id=uid,
        mark_scored=mark_scored,
        logical_score=logical_score,
        verbal_score=verbal_score,
        quant_score=quant_score,
        pass_fail=pass_fail
    )

    # Accuracy Calculation
    total_questions = int(test.test_num_of_qns)
    correct_answers = int(mark_scored)  # Assuming this stores the number of correct answers
    total_questions = int(total_questions)  # Ensure it's an integer
    accuracy = round((correct_answers / total_questions) * 100 if total_questions > 0 else 0, 0)

    print("Calculated Accuracy:", accuracy)

    #difficulty score
    
    # Convert correct_answer_ids from a comma-separated string to a list
    correct_answer_id_list = [int(q_id) for q_id in correct_answer_id.split(",") if q_id.isdigit()]

    DIFFICULTY_SCORES = {"easy": 1, "medium": 2, "hard": 3}
    question_ids = Test_Question.objects.filter(TEST_id=test_id).values_list('QUESTIONS_id', flat=True)
    questions = Questions.objects.filter(id__in=question_ids)
    
    total_difficulty_attempted = sum(DIFFICULTY_SCORES.get(q.difficulty.lower(), 0) for q in questions)

    total_difficulty_correct = sum(DIFFICULTY_SCORES.get(q.difficulty.lower(), 0) for q in questions if q.id in correct_answer_id_list)

    difficulty_score = round((total_difficulty_correct / total_difficulty_attempted) * 100 if total_difficulty_attempted > 0 else 0 , 2)

    print("Calculated Difficulty Score:", difficulty_score)

    # Improvement Rate Calculation
    previous_performances = (
    performance.objects.filter(USER_id=uid)
    .order_by("-date")
    )

    # Initialize previous accuracy value
    previous_accuracy = 0

    # Get the latest performance (most recent record)
    latest_performance = previous_performances.first()

    if latest_performance:
        previous_accuracy = float(latest_performance.accuracy)

    # Calculate improvement rate based on accuracy only
    if not latest_performance:
        improvement_rate = "NA"  # No previous data, mark as NA
    else:
        if previous_accuracy == 0:  
            improvement_rate = max(-100, min(100, round(accuracy * 100, 2)))  # Base only on current result
        else:
            improvement_rate = round(((accuracy - previous_accuracy) / previous_accuracy) * 100, 2)
            # Ensure improvement rate is within -100 to 100 range
            improvement_rate = max(-100, min(100, round(((accuracy - previous_accuracy) / previous_accuracy) * 100, 2)))

    print("Calculated Improvement Rate (Accuracy Only):", improvement_rate)

    # Store
    performance.objects.create(
        USER_id=uid,
        accuracy=str(accuracy),
        improvment_rate=str(improvement_rate),
        difficulty_score=str(difficulty_score),
        date=datetime.now().strftime("%Y%m%d%H%M%S")  # Store date in the required format
    )

    model_path = os.path.abspath(os.path.join( 'static', 'decision_tree_model.pkl'))
    model = joblib.load(model_path)
    input_data = np.array([[accuracy, float(improvement_rate) if improvement_rate != "NA" else np.nan, difficulty_score]])
    predicted_level = model.predict(input_data)[0]
    print("Predicted Level:", predicted_level)
    # Update User Progress and Level
    user = User.objects.get(id=uid)
    progress = int(user.progress)
    user_level = user.user_level

    level_map = {"Beginner": 0, "Amateur": 1000, "Professional": 2500}
    progress_change = 0
    if user_level == predicted_level:
        # Calculate Progress Change with negative improvement rate adjustment
        if improvement_rate == 0.0:
            progress_change = -10
        else:
            progress_change = 5 * (improvement_rate / 10)
    else:
        # Calculate Progress Change with negative improvement rate adjustment
        if improvement_rate>0:
            if predicted_level == "Amateur" and user_level == "Beginner":
                progress_change = 10 * (improvement_rate / 10)
            elif predicted_level == "Professional" and user_level == "Beginner":
                progress_change = 20 * (improvement_rate / 10)
            elif predicted_level == "Professional" and user_level == "Amateur":
                progress_change = 10 * (improvement_rate / 10)
            elif predicted_level == "Beginner" and user_level == "Amateur":
                progress_change = -10 * ((improvement_rate//2) / 10)
            elif predicted_level == "Beginner" and user_level == "Professional":
                progress_change = -20 * ((improvement_rate//2) / 10)
            elif predicted_level == "Amateur" and user_level == "Professional":
                progress_change = -10 * ((improvement_rate//2) / 10)
        else:
            if predicted_level == "Amateur" and user_level == "Beginner":
                progress_change = -10 * ((improvement_rate//2) / 10)
            elif predicted_level == "Professional" and user_level == "Beginner":
                progress_change = -20 * ((improvement_rate//2) / 10)
            elif predicted_level == "Professional" and user_level == "Amateur":
                progress_change = -10 * ((improvement_rate//2) / 10)
            elif predicted_level == "Beginner" and user_level == "Amateur":
                progress_change = 10 * ((improvement_rate) / 10)
            elif predicted_level == "Beginner" and user_level == "Professional":
                progress_change = 20 * ((improvement_rate) / 10)
            elif predicted_level == "Amateur" and user_level == "Professional":
                progress_change = 10 * ((improvement_rate) / 10)

    if progress_change > 0: 
        if accuracy > 80:
            progress_change = max(100, progress_change / 2) 
        elif 60 <= accuracy <= 80:
            progress_change = max(60, progress_change / 5) 
        elif 30 <= accuracy <= 60:
            progress_change = max(30, progress_change / 10)  
        elif 15 <= accuracy < 30:
            progress_change = -max(50, progress_change / 4)
        else:
            progress_change = -max(100, progress)
    progress += round(progress_change)
    progress = max(0, progress)
    # Update User Level Based on Progress
    for level, threshold in level_map.items():
        if progress >= threshold:
            user_level = level
    print("Progress Change:", progress_change)
    print("Updated Progress:", progress)
    user.progress = str(progress)
    user.user_level = user_level
    user.save()

    return JsonResponse({'status': 'ok', 'result_id': result.pk, 'progress': progress, 'user_level': user_level})

def and_get_test_results(request):
    result_id = request.POST['result_id']
    
    try:
        result = Result.objects.get(id=result_id)
        test = Test.objects.get(id=result.TEST_id)
    
        test_questions = Test_Question.objects.filter(TEST=test)
        question_details = []
        for tq in test_questions:
            question = tq.QUESTIONS
            question_details.append({
                "question": question.question,
                "correctAnswer": question.answer,
                "answerDescription": question.answer_description
            })
        
        data = {
            "testName": test.test_name,
            "testDate": test.test_date,
            "testDifficulty": test.test_difficulty,
            "totalQuestions": test.test_num_of_qns,
            "topics": test.test_topics,
            "time": test.test_time,
            "overallScore": result.mark_scored,
            "passmark": test.test_passmark,
            "isPassed": result.pass_fail.lower() == "pass",
            "topicScores": {
                "logicalScore": result.logical_score,
                "logicalTotal": test.test_num_of_qns_logical,
                "verbalScore": result.verbal_score,
                "verbalTotal": test.test_num_of_qns_verbal,
                "quantScore": result.quant_score,
                "quantTotal": test.test_num_of_qns_quantitative,
            },
            "questions_details": question_details
        }
        

        return JsonResponse({'status': 'ok', 'data': data})
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': 'error', 'message': str(e)})





from AptitudeApp.pipelines import *
import random
import nltk

# nltk.download('punkt')

# # Load question-generation model
# question_generator = pipeline("text2text-generation", model="t5-base", tokenizer="t5-base")

# def generate_questions_from_database():
#     # Fetch all questions from the database
#     all_questions = Questions.objects.all()
    
#     generated_questions = []
    
#     for q in all_questions:
#         context = f"Generate a question based on: {q.question} Answer: {q.answer}"
        
#         # Generate new question
#         new_question = question_generator(context, max_length=100, num_return_sequences=1)[0]['generated_text']
        
#         # Store in list (optional: filter for duplicates)
#         generated_questions.append({
#             'question': new_question,
#             'option1': q.optiona,
#             'option2': q.optionb,
#             'option3': q.optionc,
#             'option4': q.optiond,
#             'correctAnswer': q.answer,
#             'question_type': q.question_type,
#             'difficulty': q.difficulty
#         })

#     # Store newly generated questions in DB
#     for q in generated_questions:
#         Questions.objects.create(
#             question=q['question'],
#             optiona=q['option1'],
#             optionb=q['option2'],
#             optionc=q['option3'],
#             optiond=q['option4'],
#             answer=q['correctAnswer'],
#             question_type=q['question_type'],
#             difficulty=q['difficulty']
#         )
    
#     return {"status": "ok", "generated_questions": generated_questions}



import random
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Questions, Test, Test_Question

def and_get_test_questions_cp(request):
    # Retrieve parameters from the request
    difficulty = request.POST.get('difficulty')
    num_qns = int(request.POST.get('num_qns', 90))  # Default to 30 if not provided
    verbal = request.POST.get('verbal', '1')
    logical = request.POST.get('logical', '1')
    quant = request.POST.get('quant', '1')
    uid = request.POST.get('uid')
    time = request.POST.get('time')

    all_questions = list(Questions.objects.all())

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
    logical_count = 0
    verbal_count = 0
    quant_count = 0

    if verbal == '1':
        types_selected.append(verbal_questions)
        verbal_count = num_qns // 3  # Default division
    if logical == '1':
        types_selected.append(logical_questions)
        logical_count = num_qns // 3  # Default division
    if quant == '1':
        types_selected.append(quant_questions)
        quant_count = num_qns // 3  # Default division

    # Adjust counts for remaining questions based on the selected types
    if len(types_selected) == 1:
        if verbal == '1':
            verbal_count = num_qns
        elif logical == '1':
            logical_count = num_qns
        elif quant == '1':
            quant_count = num_qns
        selected_questions = random.sample(types_selected[0], min(num_qns, len(types_selected[0])))

    elif len(types_selected) == 2:
        type1_count = num_qns // 2
        type2_count = num_qns - type1_count
        selected_questions = random.sample(types_selected[0], min(type1_count, len(types_selected[0]))) + \
                             random.sample(types_selected[1], min(type2_count, len(types_selected[1])))
        if verbal == '1' and logical == '1':
            verbal_count = type1_count
            logical_count = type2_count
        elif verbal == '1' and quant == '1':
            verbal_count = type1_count
            quant_count = type2_count
        elif logical == '1' and quant == '1':
            logical_count = type1_count
            quant_count = type2_count

    elif len(types_selected) == 3:
        type_count = num_qns // 3
        remaining = num_qns - 2 * type_count
        selected_questions = random.sample(types_selected[0], min(type_count, len(types_selected[0]))) + \
                             random.sample(types_selected[1], min(type_count, len(types_selected[1]))) + \
                             random.sample(types_selected[2], min(remaining, len(types_selected[2])))
        verbal_count = type_count
        logical_count = type_count
        quant_count = remaining

    # Calculate test pass mark (40% of total questions)
    pass_mark = int(num_qns * 0.4)

    # Create a new Test instance
    test = Test.objects.create(
        test_name='career prediction test',
        test_date=now().strftime('%Y-%m-%d %H:%M:%S'),
        test_difficulty=difficulty,
        test_num_of_qns=num_qns,
        test_num_of_qns_logical=logical_count,
        test_num_of_qns_verbal=verbal_count,
        test_num_of_qns_quantitative=quant_count,
        test_time=time,
        test_topics=','.join(topic for topic, flag in [('Logical', logical), ('Quantitative', quant), ('Verbal', verbal)] if flag == '1'),
        test_passmark=pass_mark,
        USER_id=uid,
        cp='1'
    )

    # Map selected questions to the Test_Question table
    for question in selected_questions:
        Test_Question.objects.create(TEST=test, QUESTIONS=question)

    # Prepare final data
    questions_data = [
        {
            # 'question_id': q.id,
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

    return JsonResponse({'status': 'ok', 'data': questions_data, 'test_id': test.pk})

# def and_get_test_result(request):
#     result_id = request.POST['result_id']
    
#     try:
#         result = Result.objects.get(id=result_id)
#         test = Test.objects.get(id=result.TEST_id)
    
#         test_questions = Test_Question.objects.filter(TEST=test)
#         question_details = []
#         for tq in test_questions:
#             question = tq.QUESTIONS
#             question_details.append({
#                 "question": question.question,
#                 "correctAnswer": question.answer,
#                 "answerDescription": question.answer_description
       
#             })

#  # Accuracy Calculation
#         total_questions = test.test_num_of_qns
#         print("---------------------",total_questions)
#         correct_answers = result.mark_scored  # Assuming this stores the number of correct answers
#         print("---------------------",correct_answers)

#         accuracy = (int(correct_answers) / int(total_questions)) * 100
#         # if total_questions else 0
        
#         # Print the accuracy in the console
#         print("Calculated Accuracy:", accuracy)  


        
#         data = {
#             "testName": test.test_name,
#             "testDate": test.test_date,
#             "testDifficulty": test.test_difficulty,
#             "totalQuestions": test.test_num_of_qns,
#             "topics": test.test_topics,
#             "time": test.test_time,
#             "overallScore": result.mark_scored,
#             "passmark": test.test_passmark,
            
            
#             "isPassed": result.pass_fail.lower() == "pass",
            
            
            
#             "topicScores": {
#                 "logicalScore": result.logical_score,
#                 "logicalTotal": test.test_num_of_qns_logical,
#                 "verbalScore": result.verbal_score,
#                 "verbalTotal": test.test_num_of_qns_verbal,
#                 "quantScore": result.quant_score,
#                 "quantTotal": test.test_num_of_qns_quantitative,
#             },
#             "questions_details": question_details

#         }
        
#         return JsonResponse({'status': 'ok', 'data': data})
#     except Exception as e:
#         print(str(e))
#         return JsonResponse({'status': 'error', 'message': str(e)})

def and_post_test_results_cp(req):
    uid = req.POST["uid"]
    test_id = req.POST["test_id"]
    mark_scored = req.POST["mark_scored"]
    logical_score = req.POST["logical_score"]
    verbal_score = req.POST["verbal_score"]
    quant_score = req.POST["quant_score"]
    pass_fail = req.POST["pass_fail"]

    result = Result.objects.create(
        TEST_id=test_id,
        USER_id = uid,
        mark_scored=mark_scored,
        logical_score = logical_score,
        verbal_score = verbal_score,
        quant_score = quant_score,
        pass_fail = pass_fail
    )
    
    return JsonResponse({'status':'ok', 'result_id': result.pk})

def and_get_test_result(request):
    result_id = request.POST['result_id']
    uid = request.POST['uid']
    try:
        result = Result.objects.get(id=result_id)
        test = Test.objects.get(id=result.TEST_id)
        user = User.objects.get(id=uid)
        test_questions = Test_Question.objects.filter(TEST=test)
        question_details = []
        for tq in test_questions:
            question = tq.QUESTIONS
            question_details.append({
                "question": question.question,
                "correctAnswer": question.answer,
                "answerDescription": question.answer_description
            })
        
        data = {
            "testName": test.test_name,
            "testDate": test.test_date,
            "testDifficulty": test.test_difficulty,
            "totalQuestions": test.test_num_of_qns,
            "topics": test.test_topics,
            "time": test.test_time,
            "overallScore": result.mark_scored,
            "passmark": test.test_passmark,
            "isPassed": result.pass_fail.lower() == "pass",
            "topicScores": {
                "logicalScore": result.logical_score,
                "logicalTotal": test.test_num_of_qns_logical,
                "verbalScore": result.verbal_score,
                "verbalTotal": test.test_num_of_qns_verbal,
                "quantScore": result.quant_score,
                "quantTotal": test.test_num_of_qns_quantitative,
            },
            "questions_details": question_details
        }
        
        return JsonResponse({'status': 'ok', 'data': data , 'user_progress': user.progress, 'user_level': user.user_level})
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def and_get_results(request):
    try:
        uid = request.POST.get('uid')
        results = Result.objects.filter(USER_id=uid, TEST__cp='0')
        if not results.exists():
            return JsonResponse({'status': 'no'})
        response_data = []
        for result in results:
            test = result.TEST
            response_data.append({
                'result_id': result.id,
                'test_name': test.test_name,
                'test_date': test.test_date,
                'mark_scored': result.mark_scored,
                'pass_fail': result.pass_fail,
            })
        response_data = sorted(response_data, key=lambda x: x['test_date'], reverse=True)
        return JsonResponse({'status': 'ok', 'results': response_data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def and_get_section_test_questions(request):
    try:
        section_id = request.POST.get('section_id')
        section = Education_Content.objects.get(id=section_id)
        random_tests = list(Section_Test.objects.filter(EDUCATION_CONTENT=section))
        section_tests = random.sample(random_tests, min(3, len(random_tests)))
        questions_details = []
        for test in section_tests:
            questions_details.append({
                "question": test.question,
                "option1": test.optiona,
                "option2": test.optionb,
                "option3": test.optionc,
                "option4": test.optiond,
                "correct_answer": test.answer
            })
        response = {
            "status": "ok",
            "section_name": section.title,
            "data": questions_details,
        }
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    
def and_post_section_test_results(request):
    section_id=request.POST['section_id']
    uid=request.POST['uid']
    q=User_Educontent_Complete(EDUCATION_CONTENT_id=section_id, USER_id=uid, completed="Yes")
    q.save()
    return JsonResponse({'status':'ok'})


def and_get_test_results_prediction(request):
    result_id = request.POST['result_id']
    
    try:
        result = Result.objects.get(id=result_id)
        test = Test.objects.get(id=result.TEST_id)
    
        test_questions = Test_Question.objects.filter(TEST=test)
        question_details = []
        for tq in test_questions:
            question = tq.QUESTIONS
            question_details.append({
                "question": question.question,
                "correctAnswer": question.answer,
                "answerDescription": question.answer_description
            })
        
        data = {
            "testName": test.test_name,
            "testDate": test.test_date,
            "testDifficulty": test.test_difficulty,
            "totalQuestions": test.test_num_of_qns,
            "topics": test.test_topics,
            "time": test.test_time,
            "overallScore": result.mark_scored,
            "passmark": test.test_passmark,
            "isPassed": result.pass_fail.lower() == "pass",
            "topicScores": {
                "logicalScore": result.logical_score,
                "logicalTotal": test.test_num_of_qns_logical,
                "verbalScore": result.verbal_score,
                "verbalTotal": test.test_num_of_qns_verbal,
                "quantScore": result.quant_score,
                "quantTotal": test.test_num_of_qns_quantitative,
            },
            "questions_details": question_details
        }
        
        logicalScore = result.logical_score
        verbalScore=result.verbal_score
        quantScore=result.quant_score
        
        logicalScore_normalized = (int(logicalScore) / 30) * 100
        verbalScore_normalized = (int(verbalScore) / 30) * 100
        quantScore_normalized = (int(quantScore) / 30) * 100

        # Load the model
        model_path = os.path.abspath(os.path.join( 'static', 'career_prediction_model.pkl'))
        model = joblib.load(model_path)
        # Load the scaler
        scaler = StandardScaler()
        scaler_path = os.path.abspath(os.path.join( 'static', 'scaler.pkl'))
        scaler = joblib.load(scaler_path)
        # Provide a sample input (logical, verbal, quantitative)
        sample_input = np.array([[logicalScore_normalized,verbalScore_normalized,quantScore_normalized]])
        # Scale the input
        scaled_input = scaler.transform(sample_input)
        # Predict
        prediction = model.predict(scaled_input)
        # Convert prediction to a list if it's a NumPy array
        prediction_list = prediction.tolist() if hasattr(prediction, 'tolist') else prediction
        print(prediction_list[0])
        description = CareerPrediction.objects.get(job_role=prediction_list[0])
        return JsonResponse({'status': 'ok', 'data': data, 'result': prediction_list[0], 'description': description.job_description})

    except Exception as e:
        print(str(e))
        return JsonResponse({'status': 'error', 'message': str(e)})

#Manage Company Questions
def addcompanyquestion(request):
    if 'submit' in request.POST:
        company=request.POST['company']
        question=request.POST['question']
        answer=request.POST['answer']
        description=request.POST['description']
        q=CompanyQuestions(company_name=company,question=question,answer_description=description,answer=answer)
        q.save()
        return HttpResponse(f"<script>alert('Content added successfully');window.location='/viewcompanyquestions'</script>")
    return render(request,"admin/addcompanyquestion.html")

def viewcompanyquestions(request):
    data = CompanyQuestions.objects.all().order_by('company_name')
    grouped_data = {k: list(v) for k, v in groupby(data, key=lambda x: x.company_name)}
    return render(request, "admin/viewcompanyquestions.html", {'grouped_data': grouped_data})

def updatecompanyquestion(request, id):
    data = CompanyQuestions.objects.get(id=id)
    if 'submit' in request.POST:
        question = request.POST['question']
        answer = request.POST['answer']
        description = request.POST['description']
        company_name = request.POST['company_name']

        data.question = question
        data.answer = answer
        data.answer_description = description
        data.company_name = company_name
        data.save()
        return HttpResponse(f"<script>alert('Content updated successfully');window.location='/viewcompanyquestions'</script>")
    return render(request,"admin/updatecompanyquestion.html",{'data':data})

def deletecompanyquestion(request,id):
    data=CompanyQuestions.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert('Content deleted successfully');window.location='/viewcompanyquestions'</script>")