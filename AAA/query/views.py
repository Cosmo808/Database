
# Create your views here.
from django.core import paginator
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from . import models
from django.core.paginator import PageNotAnInteger, Paginator
import pymysql


def hello(request):
    return HttpResponse('Hello!你成功创建了一个视图！')


def hello_xiaoming(request):
    return HttpResponse('Hello！小明！')


def hello_xiaohong(request):
    return HttpResponse('Hello！小红！')


def query_patient_by_id(request,pid):
    database_name='ccc'
    #连接数据库
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    #创建一个游标
    cursor=db.cursor()
    #查询数据
    query_elements=['Age','CheckDate','Gender','PatientID']
    query_statement="select Age,CheckDate,Gender,PatientID from patientbasicinfos where id='%s'"%(pid)
    cursor.execute(query_statement)
    data=cursor.fetchall()
    #后台打印
    print(data)
    ##生成字典并返回为json格式到前端/浏览器
    data=data[0]
    out_json={}
    for j,name in enumerate(query_elements):
        out_json[name]=data[j]
    #断开连接
    db.close()
    return JsonResponse(out_json)

def patient_filter(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    query_elements=['ID','CheckDate','PatientName','Gender','Age']

    # startyear=request.POST.get('sy')
    # startmonth=request.POST.get('sm')
    # startday=request.POST.get('sd')
    # endyear=request.POST.get('ey')
    # endmonth=request.POST.get('em')
    # endday=request.POST.get('ed')
    # start=str(startyear)+'-'+str(startmonth)+'-'+str(startday)
    # end=str(endyear)+'-'+str(endmonth)+'-'+str(endday)

    # gender=str(request.POST.get('gender'))
    # age=str(request.POST.get('age'))

    #!!Sessions!!
    startyear=request.POST.get('sy')
    startmonth=request.POST.get('sm')
    startday=request.POST.get('sd')
    endyear=request.POST.get('ey')
    endmonth=request.POST.get('em')
    endday=request.POST.get('ed')
    print('startyear: ',startyear)
    start=str(startyear)+'-'+str(startmonth)+'-'+str(startday)
    print('start: ',start)
    end=str(endyear)+'-'+str(endmonth)+'-'+str(endday)

    gender=str(request.POST.get('gender'))
    age=str(request.POST.get('age'))
    print('gender: ',gender)

    page_number=request.GET.get('page')
    print('page_number: ',page_number)
    request.session['page_number']=page_number
    page_number=request.session['page_number']

    if page_number:
        start=request.session['start']
        print('session start: ',start)
        end=request.session['end']
        gender=request.session['gender']
        age=request.session['age']
    else:
        request.session['start']=start
        request.session['end']=end
        request.session['gender']=gender
        request.session['age']=age
        
    check=start+end+gender+age

    if 'None' in check or check=='----':
        if request.session.has_key('start'):
            del(request.session['start'])
        if request.session.has_key('end'):
            del(request.session['end'])
        if request.session.has_key('gender'):
            del(request.session['gender'])
        if request.session.has_key('age'):
            del(request.session['age'])
        if request.session.has_key('page_number'):
            del(request.session['page_number'])
        warning=1
        return render(request,'query/patient_filter.html',{'warning':warning,'elements':query_elements,'loop1':range(0,15),'loop2':range(0,5)})
    else:
        warning=0


    query_statement="SELECT ID, CheckDate, PatientName, Gender, Age FROM patientbasicinfos\
                    WHERE CheckDate BETWEEN '%s' and '%s' AND Gender='%s' AND Age>='%s';"%(start,end,gender,age)
    cursor.execute(query_statement)
    data=cursor.fetchall()
    output=data
    
    objects_each_page=15
    paginator=Paginator(data,objects_each_page)

    # page_number=request.GET.get('page',1)
    page_number=request.GET.get('page',1)
    request.session['page_number']=page_number
    page_number=request.session['page_number']

    page=paginator.get_page(page_number)

    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''

    if page.has_previous():
        prev_url=f'?page={page.previous_page_number()}'
    else:
        prev_url=''

    query_statement="SELECT COUNT(*) FROM patientbasicinfos  WHERE CheckDate BETWEEN '%s' and '%s' AND Gender='%s' AND Age>='%s';"%(start,end,gender,age)
    cursor.execute(query_statement)
    number=cursor.fetchall()
    number=str(number[0][0])

    if number=='0' :
        error=1
        return render(request,'query/patient_filter.html',{'error':error,'elements':query_elements,'loop1':range(0,15),'loop2':range(0,5)})
    else:
        error=0

    return render(request,'query/patient_filter.html',{'rlt':output,'elements':query_elements,'number':number,'error':error,
                                                        'page':page,'next_page_url':next_url, 'prev_page_url':prev_url})


def ill_doctor_filter(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    pathtype=str(request.POST.get('pathtype'))
    doctor=str(request.POST.get('doctor'))

    query_elements=['ID', 'ImageID', 'Pathtype', 'UserID', 'PatientID']
    query_statement="SELECT ID, ImageID, Pathtype, UserID, PatientID FROM d_labeledimage\
                    WHERE Pathtype='%s' AND UserID='%s';"%(pathtype,doctor)
    cursor.execute(query_statement)
    data=cursor.fetchall()
    output=data

    query_statement="SELECT COUNT(*) FROM d_labeledimage WHERE Pathtype='%s' AND UserID='%s';"%(pathtype,doctor)
    cursor.execute(query_statement)
    number=cursor.fetchall()
    number=str(number[0][0])

    return render(request,'query/ill_doctor_filter.html',{'rlt':output,'number':number,'elements':query_elements})

def anatomy_doctor_filter(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    pathtype=str(request.POST.get('pathtype'))
    doctor=str(request.POST.get('doctor'))

    query_elements=['ID', 'ImageID', 'ImgPath', 'Pathtype', 'UserID', 'PatientID']
    query_statement="SELECT a.ID, a.ImageID, i.ImgPath, a.Pathtype, a.UserID, a.PatientID FROM a_labeledimage a\
                    INNER JOIN imgpath i\
                    ON a.Pathtype='%s' AND a.UserID='%s' AND a.ImageID=i.ImageID;"%(pathtype,doctor)
    cursor.execute(query_statement)
    data=cursor.fetchall()
    output=data

    return render(request,'query/anatomy_doctor_filter.html',{'rlt':output,'elements':query_elements})

def ill_gender_hospital_filter_exam(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    ill=str(request.POST.get('ill'))
    gender=str(request.POST.get('gender'))
    hospital=str(request.POST.get('hospital'))

    query_elements=['ID', 'PatientName', 'Gender', 'PatientID', 'AreaID', 'DiseaseName', 'InstituteName']
    query_statement="SELECT p.ID, p.PatientName, p.Gender, p.PatientID, dl.AreaID, dd.DiseaseName, h.InstituteName\
                    FROM patientbasicinfos p\
                    INNER JOIN (hospital_record h, disease_dict dd, d_arearoi da, d_labeledimage dl)\
                    ON p.Gender='%s' AND h.InstituteName='%s' AND p.HospitalID=h.InstituteID \
                    AND dd.DiseaseName='%s' AND dd.DiseaseID=da.DiseaseID AND dl.AreaID=da.AreaID AND p.PatientID=dl.PatientID;"%(gender, hospital, ill)
    cursor.execute(query_statement)
    data=cursor.fetchall()
    output=data

    return render(request,'query/ill_gender_hospital_filter_exam.html',{'rlt':output,'elements':query_elements})


def query_patient(request):
    # if request.method=='POST':
        pid=request.POST.get('patientid')
        if pid==None or pid=='':
            error=0
            warning=1
            return render(request,'query/query_patient.html',{'error':error,'warning':warning})
        else:
            warning=0

        try:
            user=models.Patientbasicinfos.objects.filter(id=pid).first()
            age=user.age
            error=0
        except:
            error=1
            return render(request,'query/query_patient.html',{'error':error,'warning':warning})

        age=user.age
        checkdate=user.checkdate
        gender=user.gender
        # return render(request, 'query/query_patient.html')
        return render(request,'query/query_patient.html',{'id':pid,'age':age,'checkdate':checkdate,'gender':gender,'error':error,'warning':warning})
    # else:
    #     return HttpResponse('ERROR')

def bootstrap_demo(request):
    return render(request,'bootstrap_demo.html')

## 去重函数 只对Patientbasicinfos进行查重，因为imagepath中一个PatientID对应多个imageID，且未重复##
def QuChong():
    #如果PatientID与Checknumber一致，则只保留最后一条
    dbname='Patientbasicinfos'
    for row in models.dbname.objects.all():
        if models.Patientbasicinfos.objects.filter(patientid=row.patientid,checknumber=row.checknumber).count() > 1:
            row.delete()
    #如果PatientID与Checknumber不一致，则后面的数据PatientID+1
    for row in models.Patientbasicinfos.objects.all():
        if models.Patientbasicinfos.objects.filter(patientid=row.patientid).count() > 1:
            cnt1 = 0
            obj = models.Patientbasicinfos.objects.filter(patientid=row.patientid)
            for row1 in obj:
                Pid = int(row1.patientid)
                Pid +=cnt1
                cnt1+=1
                row1.patientid=str(Pid)
                row1.save()


def cosmo(request):
    return render(request,'cosmo.html')

def normalentry(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    Account=str(request.POST.get('account'))
    Passward=str(request.POST.get('passward'))

    login_statement="SELECT Account, Passward FROM Administrator\
                    WHERE Account='%s' AND Passward='%s';"%(Account,Passward)
    cursor.execute(login_statement)
    user=cursor.fetchall()
    print(user)
    if user:
        return redirect('http://127.0.0.1:8000/normalquery/')
    else:
        return render(request,'normalentry.html')

def administratorlogin(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    Account=str(request.POST.get('account'))
    Passward=str(request.POST.get('passward'))

    login_statement="SELECT Account, Passward FROM Administrator\
                    WHERE Account='%s' AND Passward='%s';"%(Account,Passward)
    cursor.execute(login_statement)
    user=cursor.fetchall()
    if user:
        return redirect('http://127.0.0.1:8000/adminquery/')
    else:
        return render(request,'administratorlogin.html')


def normalregister(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    Account=str(request.POST.get('account'))
    Passward=str(request.POST.get('passward'))

    if 'None' in Account+Passward or Account=='' or Passward=='':
        return render(request,'normalregister.html')

    register_statement="INSERT INTO Administrator (Account,Passward) VALUES ('%s','%s');"%(Account,Passward)
    cursor.execute(register_statement)
    cursor.execute("COMMIT;")

    return redirect('http://127.0.0.1:8000/normalentry/')

def administratorregister(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    Account=str(request.POST.get('account'))
    Passward=str(request.POST.get('passward'))
    Check=str(request.POST.get('check'))

    admin_check='123456'

    if 'None' in Account+Passward or Account=='' or Passward=='' or Check!=admin_check:
        return render(request,'administratorregister.html')

    register_statement="INSERT INTO Administrator (Account,Passward) VALUES ('%s','%s');"%(Account,Passward)
    cursor.execute(register_statement)
    cursor.execute("COMMIT;")

    return redirect('http://127.0.0.1:8000/administratorlogin/')


def nologinquery(request):
    return render(request,'loginquery/nologinquery.html')

def normalquery(request):
    return render(request,'loginquery/normalquery.html')

def adminquery(request):
    return render(request,'loginquery/adminquery.html')


#动态分页
def pagination(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    login_statement="SELECT * FROM Patientbasicinfos"
    cursor.execute(login_statement)
    posts=cursor.fetchall()

    objects_each_page=8
    paginator=Paginator(posts,objects_each_page)
    page_number=request.GET.get('page',1)
    page=paginator.get_page(page_number)

    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''

    if page.has_previous():
        prev_url=f'?page={page.previous_page_number()}'
    else:
        prev_url=''

    return render(request, 'pagination.html', context={'page':page, 
                                            'next_page_url':next_url, 'prev_page_url':prev_url})

 
def admin_insert(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    pid=str(request.POST.get('pid'))
    checkdate=str(request.POST.get('checkdate'))
    patientid=str(request.POST.get('patientid'))
    patientname=str(request.POST.get('patientname'))
    gender=str(request.POST.get('gender'))
    age=request.POST.get('age')


    data_all=[pid,checkdate,patientid,patientname,gender,age]
    element_all=['id','checkdate','patientid','patientname','gender','age']

    data_notnone=[]
    ele_notnone=[]
    check=''
    i=0

    for data in data_all:
        if data and data!='None':
            data_notnone.append(data_all[i])
            ele_notnone.append(element_all[i])
        i=i+1
        check=check+str(data)

    if 'None' in check or check=='':
        error=0
        warning=1
        return render(request,'admin_insert.html',{'error':error,'warning':warning})
    else:
        warning=0

    elem=''
    for ele in ele_notnone:
        elem=elem+ele+','
    #去掉最后一个逗号
    ele=list(elem)
    ele[(len(elem)-1)]=''
    elem=''.join(ele)

    data=''
    for dat in data_notnone:
        data=data+"'"+dat+"'"+','
    dat=list(data)
    dat[len(data)-1]=''
    data=''.join(dat)

    try:
        user=models.Patientbasicinfos.objects.filter(id=pid).first()
        print(user.id)  #查询该id是否已被占用，若不报错则被占用
        error=1
        return render(request,'admin_insert.html',{'error':error,'warning':warning})
    except:
        error=0
        #寻找用户报错说明可以插入新用户
        insert_statement="INSERT INTO patientbasicinfos (%s) VALUES (%s);"%(elem,data)
        cursor.execute(insert_statement)
        cursor.execute("COMMIT;")
        return render(request,'admin_insert.html',
                  {'pid':pid,'checkdate':checkdate,'patientid':patientid,'patientname':patientname,
                   'gender':gender,'age':age,'error':error,'warning':warning})



def admin_delete(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    pid=request.POST.get('patientid')

    if 'delete' in request.GET:
        if request.session.has_key('pid'):
            pid=request.session['pid']
            del(request.session['pid'])
            error=0
            warning=0
            statement="DELETE FROM patientbasicinfos WHERE id='%s';"%(pid)
            cursor.execute(statement)
            cursor.execute("COMMIT;")
            notice='删除成功！'
            return render(request,'admin_delete.html',{'error':error,'warning':warning,"notice":notice})

    if pid=='None' or pid=='':
        error=0
        warning=1
        return render(request,'admin_delete.html',{'error':error,'warning':warning})
    else:
        warning=0
        request.session['pid']=pid

    try:
        user=models.Patientbasicinfos.objects.filter(id=pid).first()
        age=user.age
        error=0
    except:
        error=1
        return render(request,'admin_delete.html',{'error':error,'warning':warning})

    checkdate=user.checkdate
    patientid=user.patientid
    patientname=user.patientname
    gender=user.gender
    age=user.age

    elements=['ID','checkdate','patientid','patientname','gender','age']
    notice='请确认是否删除该病人信息!'
    return render(request,'admin_delete.html',
                  {'pid':pid,'checkdate':checkdate,'patientid':patientid,'patientname':patientname,
                   'gender':gender,'age':age,'error':error,'warning':warning,'notice':notice})


def admin_update(request):
    database_name='ccc'
    db=pymysql.connect(host="localhost",user="root",password="root",db=database_name,)
    cursor=db.cursor()

    pid=str(request.POST.get('patientid'))
    checkdate=str(request.POST.get('checkdate'))
    clinicaldiagnosis=str(request.POST.get('clinicaldiagnosis'))
    examinationfindings=str(request.POST.get('examinationfindings'))
    endoscopicdiagnosis=str(request.POST.get('endoscopicdiagnosis'))
    pathologicaldiagnosis=str(request.POST.get('pathologicaldiagnosis'))

    data_all=[checkdate,clinicaldiagnosis,examinationfindings,
                endoscopicdiagnosis,pathologicaldiagnosis]
    # element_all=['CheckDate','ClinicalDiagnosis','ExaminationFindings',
    #             'EndoscopicDiagnosis','PathologicalDiagnosis']
    element_all=['checkdate','clinicaldiagnosis','examinationfindings',
                'endoscopicdiagnosis','pathologicaldiagnosis']
    data_notnone=[]
    ele_notnone=[]
    check=''
    i=0

    for data in data_all:
        if data and data!='None':
            data_notnone.append(data_all[i])
            ele_notnone.append(element_all[i])
        i=i+1
        check=check+data

    if 'None' in check or check=='':
        error=0
        warning=1
        return render(request,'admin_update.html',{'error':error,'warning':warning})
    else:
        warning=0

    elem=''
    for ele in ele_notnone:
        elem=elem+ele+','
    #去掉最后一个逗号
    ele=list(elem)
    ele[(len(elem)-1)]=''
    elem=''.join(ele)

    data=''
    for dat in data_notnone:
        data=data+"'"+dat+"'"+','
    dat=list(data)
    dat[len(data)-1]=''
    data=''.join(dat)

    print(elem)
    print(data)
    try:
        user=models.Patientbasicinfos.objects.filter(id=pid).first()
        patientid=user.patientid
        patientname=user.patientname
        gender=user.gender
        age=user.age
        error=0
    except:
        error=1
        return render(request,'admin_update.html',{'error':error,'warning':warning})

    l=len(data_notnone)
    for i in range(0,l):
        update_statement="UPDATE patientbasicinfos SET %s = (%s) WHERE id='%s';"%(ele_notnone[i],data_notnone[i],pid)
        cursor.execute(update_statement)
        cursor.execute("COMMIT;")

    return render(request,'admin_update.html',{'error':error,'warning':warning,'pid':pid,'checkdate':checkdate,
                                        'clinicaldiagnosis':clinicaldiagnosis,'examinationfindings':examinationfindings,
                                        'endoscopicdiagnosis':endoscopicdiagnosis,'pathologicaldiagnosis':pathologicaldiagnosis,
                                        'patientid':patientid,'patientname':patientname,'gender':gender,'age':age})