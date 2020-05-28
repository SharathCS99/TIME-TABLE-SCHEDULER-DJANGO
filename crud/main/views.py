from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import path,include
from firebase import firebase
from .forms import student_form
from django.contrib import messages
from .forms import *
firebase=firebase.FirebaseApplication('https://nodemcu-15321.firebaseio.com/')
a=['id','pass','pass2','slot']
dictimes=[]
dictimep=[]
temslots=[]
x=0
reg_id=0
id=0
a1=['mon','tue','wed','thu','fri','sat','sun']
loga=['id1','pass1']
def startup(request):
	return render(request,'stata.html')
def login(request):
	global loga
	return render(request,'LOG.html',{'id1':loga[0],'pass1':loga[1]})
def updater(request):
	global loga
	global a
	return render(request,'LOG1.html',{'id1':loga[0],'pass1':loga[1],'slot':a[0]})
def updateo(request):
	global x
	global a
	global id
	global dictimes
	dictimes=[]
	a[0]=request.GET['id1']
	if(firebase.get('/'+str(request.GET['id1']),'id')!=None):
		if(firebase.get('/'+str(request.GET['id1']),'pass')==request.GET['pass1']):
			x=int(request.GET['slot'])
			reg_id=request.GET['id1']
			s="/"+str(reg_id)
			id=s
			print(s,"is id here")
			firebase.patch(s,{'slot':x})
			tb=firebase.delete(s,'table')
		else:
			messages.error(request,"the paswords or username do not match or no such user")
			return redirect('update1')
		for i in range(0,x):
			con='slote'+str(i)
			dictimes.append(con)
		return render(request,'filluptime.html',{'times':dictimes})
	else:
		messages.error(request,"the paswords or username do not match or no such user")
		return redirect('update1')
def actuallo(request):
	global x
	if(firebase.get('/'+str(request.GET['id1']),'id')!=None):
		if(firebase.get('/'+str(request.GET['id1']),'pass')==request.GET['pass1']):
			reg_id=request.GET['id1']
			print(reg_id)
			temslots=[]
			dic=firebase.get('/'+str(request.GET['id1'])+'/'+'table','mon')
			print(dic)
			try:
				for i in dic.keys():
					temslots.append(i)
				mon=[]
				tue=[]
				wed=[]
				thu=[]
				fri=[]
				sat=[]
				sun=[]
				dic=firebase.get(reg_id,'table')
				print(dic)
				print(temslots)
				for i in dic.get('mon').values():
					mon.append(i)
				for i in dic.get('tue').values():
					tue.append(i)
				for i in dic.get('wed').values():
					wed.append(i)
				for i in dic.get('thu').values():
					thu.append(i)
				for i in dic.get('fri').values():
					fri.append(i)
				for i in dic.get('sat').values():
					sat.append(i)
				for i in dic.get('sun').values():
					sun.append(i)
				print(wed)
				return render(request,'tab.html',{'mon':mon,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun,'a1':a1,'tem':temslots})
			except:
				messages.error(request,"no table found")
				return redirect('login')
		else:
			messages.error(request,"the paswords or username do not match or no such user")
			return redirect('login')
	else:
		messages.error(request,"the paswords or username do not match or no such user")
		return redirect('login')
def home(request):
	global a
	d={'id':a[0],'pass':a[1],'pass2':a[2],'slot':a[3]}
	return render(request,'home.html',d)
def exp(request):
	my_form=student_form()
	my_form.de(10)
	print(request.method=="POST")
	if request.method=="POST":
		my_form=student_form(request.POST)
		if my_form.is_valid():
			print(my_form.cleaned_data)
		else:
			print(my_form.errors)
	context={"form":my_form}
	return render(request,'studentform.html',context)
def addtime(request):
	global a
	global reg_id
	reg_id=request.GET[a[0]]
	d=firebase.get('/'+str(reg_id),'id')
	print(d)
	if(d!=None):
		print("hey")
		messages.error(request,"This user already present please login")
		return redirect('startup')
	print(reg_id)
	print("infuncton")
	global x
	x=int(request.GET[a[3]])
	global id
	global dictimes
	dictimes=[]
	if(request.GET[a[1]]!=request.GET[a[2]]):
		messages.error(request,"the paswords do not match")
		return redirect('home')
	if((len(request.GET[a[1]])<8)or not(('*' in request.GET[a[1]])or('@' in request.GET[a[1]])or('#' in request.GET[a[1]]))):
		messages.error(request,"enter a stronger pasword minimum length 8 with special characters")
		return redirect('home')

	if(request.GET[a[3]]==''):
		messages.error(request,"the slot field must not be empty")
		return redirect('home')
	else:
		for i in a:
			s='/'+str(request.GET[a[0]])
			firebase.patch(s,{i:request.GET[i]})
		for i in range(0,x):
			con='slote'+str(i)
			dictimes.append(con)
		id=s
		return render(request,'filluptime.html',{'times':dictimes})
def add(request):
	global a
	global x
	global temslots
	temslots=[]
	global dictimep
	dictimep=[]
	global a1
	for i in range(0,x):
		con='cont'+str(i)
		dictimep.append(con)
	for i in dictimes:
		temslots.append(request.GET[i])
	print(temslots)
	return render(request,'fillup.html',{'dic1':dictimep,'dic2':a1})
def done(request):
	global reg_id
	print(reg_id)
	global dictimep
	global temslots
	global a1
	global dictimes
	global id
	s=str(id)+'/table'
	k=s
	mon=[]
	tue=[]
	wed=[]
	thu=[]
	fri=[]
	sat=[]
	sun=[]
	for i in a1:
		s=s+'/'+str(i)
		print(s)
		for j in temslots:
			firebase.patch(s,{j:request.GET[i+'+'+dictimep[temslots.index(j)]]})
		s=k
	reg_id='/'+str(reg_id)
	print(reg_id)
	dic=firebase.get(reg_id,'table')
	print(dic)
	print(temslots)
	for i in dic.get('mon').values():
		mon.append(i)
	for i in dic.get('tue').values():
		tue.append(i)
	for i in dic.get('wed').values():
		wed.append(i)
	for i in dic.get('thu').values():
		thu.append(i)
	for i in dic.get('fri').values():
		fri.append(i)
	for i in dic.get('sat').values():
		sat.append(i)
	for i in dic.get('sun').values():
		sun.append(i)
	print(wed)
	return render(request,'tab.html',{'mon':mon,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun,'a1':a1,'tem':temslots})
