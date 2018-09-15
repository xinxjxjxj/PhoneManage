#coding=utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Phone.models import Android, iOS, borrowHistory
import csv,codecs,time



# index返回登录
def index(request):
    username = request.session.get('user', '')
    if username:
        return HttpResponseRedirect('/home/')
    else:
        return render(request, 'index.html')

def login(request):
    username = request.session.get('user', '')
    if username:
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/Android_list/')

# 登录
def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/home/')
            return response
        else:
            return render(request, "index.html", {'error':'账号或密码错误！'})
 
# 未登录返回安卓设备列表，提供申请和取消申请
def Android_list(request):
#     返回搜索栏下拉菜单值
    agent = request.META.get('HTTP_USER_AGENT','')
    brands_list = Android.objects.values('brand').distinct()
    sizes_list = Android.objects.values('Physical_size').distinct()
    Androids = Android.objects.all().order_by('-breakdown')
#     分页
    paginator = Paginator(Androids,100)
    page = request.GET.get('page')
    try:
        Androids = paginator.page(page)
    except PageNotAnInteger:
        Androids = paginator.page(1)
    except EmptyPage:
        Androids = paginator.page(paginator.num_pages)
    username = request.session.get('user', '')
    context = {"user":username, "Androids":Androids, "brands_list":brands_list,"sizes_list":sizes_list,"agent":agent}
    return render(request,"Android_list.html", context)        

def iOS_list(request):
    iOSs = iOS.objects.all().order_by('-breakdown')
    paginator = Paginator(iOSs,50)
    page = request.GET.get('page')
    try:
        iOSs = paginator.page(page)
    except PageNotAnInteger:
        iOSs = paginator.page(1)
    except EmptyPage:
        iOSs = paginator.page(paginator.num_pages)
    username = request.session.get('user', '')
    context = {"user":username, "iOSs":iOSs}
    return render(request,"iOS_list.html", context)

# 借用记录需登录，按借用时间正序排序
@login_required    
def history_list(request):
    history_lists = borrowHistory.objects.all().order_by("-id")
    paginator = Paginator(history_lists,20)
    page = request.GET.get('page')
    print paginator
    try:
        history_lists = paginator.page(page)
    except PageNotAnInteger:
        history_lists = paginator.page(1)
    except EmptyPage:
        history_lists = paginator.page(paginator.num_pages)
    username = request.session.get('user', '')
    context = {"user":username, "history_lists":history_lists}
    return render(request,"history_list.html",context)
 
#    管理员登录，提供借出和归还操作
@login_required        
def Android_manage(request):
    brands_list = Android.objects.values('brand').distinct()
    sizes_list = Android.objects.values('Physical_size').distinct()
    Androids = Android.objects.all().order_by('-breakdown')
    paginator = Paginator(Androids,100)
    page = request.GET.get('page')
    try:
        Androids = paginator.page(page)
    except PageNotAnInteger:
        Androids = paginator.page(1)
    except EmptyPage:
        Androids = paginator.page(paginator.num_pages)
    username = request.session.get('user', '')
    context = {"user":username, "Androids":Androids, "brands_list":brands_list,"sizes_list":sizes_list}
    return render(request,"Android_manage.html",context)

@login_required        
def iOS_manage(request):
    iOSs = iOS.objects.all().order_by('-breakdown')
    paginator = Paginator(iOSs,50)
    page = request.GET.get('page')
    try:
        iOSs = paginator.page(page)
    except PageNotAnInteger:
        iOSs = paginator.page(1)
    except EmptyPage:
        iOSs = paginator.page(paginator.num_pages)
    username = request.session.get('user', '')
    return render(request,"iOS_manage.html",{"user":username, "iOSs":iOSs})
 
#    搜索 
def search(request):
    username = request.session.get('user', '')
    search_id = request.GET.get('id', '')
    search_brand = request.GET.get('brand', '')
    search_version = request.GET.get('version','')
    search_size = request.GET.get('size','')
    search_name = request.GET.get('name','')
    search_owner = request.GET.get('owner','')
    if "Android" in search_id:
        brands_list = Android.objects.values('brand').distinct()
        Androids = Android.objects.filter(brand__contains=search_brand,Android_version__contains=search_version,Physical_size__contains=search_size).order_by('-breakdown')
        context = {"user":username,"Androids":Androids,"brand1":search_brand,"version1":search_version,"size1":search_size, "brands_list":brands_list}
        if username :
            return render(request, "Android_manage.html", context)
        else:
            return render(request, "Android_list.html", context)
    elif "iOS" in search_id:
        iOSs = iOS.objects.filter(name__contains=search_name,iOS_version__contains=search_version).order_by('-breakdown')
        context = {"user":username,"iOSs":iOSs, 'name1':search_name, 'version1':search_version}
        if username:
            return render(request, "iOS_manage.html", context)
        else:
            return render(request, "iOS_list.html", context)
    elif "history" in search_id:
        history_lists = borrowHistory.objects.filter(devicename__contains=search_name,owner__contains=search_owner).order_by("-modifiedtime")
        context = {"user":username,'history_lists':history_lists, 'name':search_name, 'owner':search_owner}
        return render(request, "history_list.html", context)
    
# 管理员借出
@login_required     
def borrow(request): 
    username = request.session.get('user', '')
    input_id = request.POST.get('id','')
    input_name = request.POST.get('ownerinput','')
    input_brand = request.POST.get('brand','')
    if input_name:
        if input_brand:
            borrow = Android.objects.get(id=input_id)
        else:
            borrow = iOS.objects.get(id=input_id)
        borrow.owner=input_name
        borrow.status='0'
        borrow.applicant=''
        borrow.save()
        #新增操作记录
        borrowHistory.objects.create(devicename=borrow.name,owner=input_name,managername=username,status='0')
        if input_brand:
            return HttpResponseRedirect('/Android_manage/') 
        else:
            return HttpResponseRedirect('/iOS_manage/') 

@login_required  
def homeborrow(request): 
    username = request.session.get('user', '')
    input_id = request.POST.get('id','')
    input_name = request.POST.get('ownerinput','')
    input_brand = request.POST.get('brand','')
    if input_name:
        if input_brand:
            borrow = Android.objects.get(id=input_id)
        else:
            borrow = iOS.objects.get(id=input_id)
        borrow.owner=input_name
        borrow.status='0'
        borrow.applicant=''
        borrow.save()
        #新增操作记录
        borrowHistory.objects.create(devicename=borrow.name,owner=input_name,managername=username,status='0')
        return HttpResponseRedirect('/home/') 

# 管理员拒绝    
@login_required     
def reject(request): 
    input_id = request.POST.get('id','')
    input_brand = request.POST.get('brand','')
    if input_brand:
        Android.objects.filter(id=input_id).update(applicant='')
        return HttpResponseRedirect('/Android_manage/') 
    else:
        iOS.objects.filter(id=input_id).update(applicant='')
        return HttpResponseRedirect('/iOS_manage/') 
 
#  管理员归还   
@login_required     
def back(request): 
    input_id = request.POST.get('id','')
    input_brand = request.POST.get('brand','')    
    if input_brand:
        android = Android.objects.get(id=input_id)
        Android.objects.filter(id=input_id).update(owner='',status='1')
        #新增操作记录
        borrowHistory.objects.create(devicename=android.name,owner=android.owner,managername='admin',status='1')
        return HttpResponseRedirect('/Android_manage/') 
    else:
        ios = iOS.objects.get(id=input_id)
        iOS.objects.filter(id=input_id).update(owner='',status='1')
        borrowHistory.objects.create(devicename=ios.name,owner=ios.owner,managername='admin',status='1')
        return HttpResponseRedirect('/iOS_manage/')

# 申请手机
def apply_list(request):
    apply_id = request.POST.get('id','')
    apply_brand = request.POST.get('brand','')
    apply_name = request.POST.get('applyname','')
    if apply_brand:
        if apply_name:
            Android.objects.filter(id=apply_id).update(applicant=apply_name)
        return HttpResponseRedirect('/Android_list/')
    else:
        if apply_name:
            iOS.objects.filter(id=apply_id).update(applicant=apply_name)
        return HttpResponseRedirect('/iOS_list/')

# 取消申请        
def apply_cancel(request):
    apply_id = request.POST.get('id','')
    apply_brand = request.POST.get('brand','')
    if apply_brand:
        Android.objects.filter(id=apply_id).update(applicant='')
        return HttpResponseRedirect('/Android_list/')
    else:
        iOS.objects.filter(id=apply_id).update(applicant='')
        return HttpResponseRedirect('/iOS_list/')
    
#报修
def breakdown(request):
    apply_id = request.POST.get('id','')
    apply_brand = request.POST.get('brand','')
    if apply_brand:
        android = Android.objects.get(id=apply_id)
        #如在使用先归还
        if android.owner:
            borrowHistory.objects.create(devicename=android.name,owner=android.owner,managername='admin',status='1')
        Android.objects.filter(id=apply_id).update(breakdown='0',status='1',owner='')
        return HttpResponseRedirect('/Android_manage/')
    else:
        ios = iOS.objects.get(id=apply_id)
        if ios.owner:
            borrowHistory.objects.create(devicename=ios.name,owner=ios.owner,managername='admin',status='1')
        iOS.objects.filter(id=apply_id).update(breakdown='0',status='1',owner='')
        return HttpResponseRedirect('/iOS_manage/')
 
#修复
def repair(request):
    apply_id = request.POST.get('id','')
    apply_brand = request.POST.get('brand','')
    if apply_brand:
        Android.objects.filter(id=apply_id).update(breakdown='1')
        return HttpResponseRedirect('/Android_manage/')
    else:
        iOS.objects.filter(id=apply_id).update(breakdown='1')
        return HttpResponseRedirect('/iOS_manage/')
    
#导出手机列表
def export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=测试机清单.csv'
    response.write(codecs.BOM_UTF8)
    Androids = Android.objects.all()
    iOSs = iOS.objects.all()
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    writer = csv.writer(response)
    writer.writerow(['测试机清单','日期：'+time1])
    writer.writerow(['编号', '品牌','型号','系统版本','屏幕分辨率','资产编号','状态','借用人','借用历史'])
    for iOS1 in iOSs:
        iosname = iOS1.name.encode('utf-8') + ' ' + iOS1.version.encode('utf-8')
        borrownameslist = [borrowname.owner for borrowname in borrowHistory.objects.filter(devicename=iOS1.name,status='1').order_by("-id")]
        borrownames = ','.join(borrownameslist).encode('utf-8')
        writer.writerow([iOS1.id, '苹果',iosname,iOS1.iOS_version.encode('utf-8'),iOS1.Physical_size.encode('utf-8'),iOS1.assetnum.encode('utf-8'),'',iOS1.owner.encode('utf-8'),borrownames])
    
    for Android1 in Androids:
        borrownameslist = [borrowname.owner for borrowname in borrowHistory.objects.filter(devicename=Android1.name,status='1').order_by("-id")]
        borrownames = ','.join(borrownameslist)
        writer.writerow([Android1.id+len(iOSs), Android1.brand.encode('utf-8'),Android1.name.encode('utf-8'),Android1.Android_version.encode('utf-8'),Android1.Physical_size.encode('utf-8'),Android1.assetnum.encode('utf-8'),'',Android1.owner.encode('utf-8'),borrownames.encode('utf-8')])
    return response

@login_required 
def home(request):
    history_lists = borrowHistory.objects.all().order_by("-id")[:10]
    Android_Borrowed_count = Android.objects.filter(status=0,breakdown='1').count()
    Android_Available_count = Android.objects.filter(status=1,breakdown='1').count()
    Android_broken = Android.objects.filter(breakdown='0').count()
    Android_count = Android.objects.count()
    iOS_Borrowed_count = iOS.objects.filter(status=0,breakdown='1').count()
    iOS_Available_count = iOS.objects.filter(status=1,breakdown='1').count()
    iOS_broken = iOS.objects.filter(breakdown='0').count()
    iOS_count = iOS.objects.count()
    Phones = Android.objects.exclude(applicant="")
    iOSapply = iOS.objects.exclude(applicant="")
    data = {}
    data1 = {}
    paginator = Paginator(history_lists,20)
    page = request.GET.get('page')
    try:
        history_lists = paginator.page(page)
    except PageNotAnInteger:
        history_lists = paginator.page(1)
    except EmptyPage:
        history_lists = paginator.page(paginator.num_pages)
    username = request.session.get('user', '')
    if Android_count >0:
        data = {"Android_Available_rate":Android_Available_count*100/Android_count,"Android_Borrowed_rate":Android_Borrowed_count*100/Android_count,"Android_broken_rate":100-Android_Available_count*100/Android_count-Android_Borrowed_count*100/Android_count,"Android_count":Android_count,"Android_Borrowed_count":Android_Borrowed_count,"Android_broken":Android_broken}
    if iOS_count >0:
        data1 = {"iOS_Available_rate":iOS_Available_count*100/iOS_count,"iOS_Borrowed_rate":iOS_Borrowed_count*100/iOS_count,"iOS_broken_rate":100-iOS_Available_count*100/iOS_count-iOS_Borrowed_count*100/iOS_count,"iOS_count":iOS_count,"iOS_Borrowed_count":iOS_Borrowed_count,"iOS_broken":iOS_broken}
    context = {"data":data,"data1":data1,"user":username, "history_lists":history_lists,"Phones":Phones,"iOSapply":iOSapply}
    return render(request, "home.html", context)

#  退出登录   
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

# 404和500页面
def page_not_found(request):
    return HttpResponseRedirect('/Android_list/')

def page_error(request):
    return HttpResponseRedirect('/Android_list/')