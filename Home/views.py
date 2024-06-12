from django.shortcuts import render, redirect
from django.http import JsonResponse
import pyrebase
from django.views.decorators.cache import cache_control
import os, json

FirebaseConfig={
    "apiKey": os.environ['apiKey'],
    "authDomain": os.environ['authDomain'],
    "databaseURL": os.environ['databaseURL'],
    "projectId": os.environ['projectId'],
    "storageBucket": os.environ['storageBucket'],
    "messagingSenderId": os.environ['messagingSenderId'],
    "appId": os.environ['appId']
}

firebase=pyrebase.initialize_app(FirebaseConfig)
db=firebase.database()
auth=firebase.auth()
storage=firebase.storage()


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['pswd']
        try:
            auth.sign_in_with_email_and_password(email,password)
            print("signed in")
            data=db.child("Student").order_by_child("mail").equal_to(email).get()
            jdata=data.each()[0].val()
            fileName=jdata['RollNo']+".jpg"
            # jdata=json.dumps(data.each()[0].val(), indent = 4)
            appoint = db.child("Appointment").get()
            appoint=appoint.val()
            print(appoint)
            url=storage.child(fileName).get_url(None)
            return render(request,"index.html",{"img":url,'data':jdata,'appoint':sorted(appoint.items())})
        except Exception as e:
            print(e)
            return render(request,"home.html",{"msg":"Wrong Password"})
    else:
        return render(request,"home.html")
    
def resetPassword(request):
    email=request.GET.get('email',None)
    auth.send_password_reset_email(email)
    return JsonResponse({'message': 'Form data received successfully.'})

def logout(request):
    try:
        auth.current_user = None
        # del request.session['token_id']
    except KeyError:
        pass
    return redirect('/')


def search(request):
    teacherName=request.GET['teacherName']
    rollno=request.GET['rollno']
    name=request.GET['name']
    data={
        "rollno":rollno,
        "name":name
    }
    if teacherName=='anup':
        return render(request,"search.html",{'data':data})
    else:
        return JsonResponse({'message': 'no teacher exist'})
    

def MakeAppointment(request):
    reason=request.GET.get('reason',None)
    rollno=request.GET.get('rollno',None)
    name=request.GET.get('name',None)
    data={
        'Reason':reason,
        'RollNo':rollno,
        'name':name,
        'status':'No'
    }
    db.child('Appointment').push(data)
    return JsonResponse({'message': 'Form data received successfully.'})