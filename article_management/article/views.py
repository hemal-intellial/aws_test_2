from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Article
from tag.models import Tag
from article_tag.models import Article_tag
from django.contrib import auth
# Create your views here.
def article(request):
    return render(request,"article.html")


def article_publish(request,id=None):
    if request.method == 'POST':
        user_id  = request.user.id
        title = request.POST['title']
        content = request.POST['content']
            
        tag = request.POST['tag']
        tag_name = tag.split(',')
        
        tags = list(Tag.objects.filter(tag_name__in = tag_name).values_list("tag_name",flat=True))

        for x in tags:
            tag_name.remove(x)
        print(tag_name,"tag_name")
            
        Tag.objects.bulk_create([Tag(tag_name=x) for x in tag_name])
        if id==None:
            if 'publish' in request.POST:
                article=Article(user_id=user_id,title=title,content=content)
                article.save()
            else:
                article=Article(user_id=user_id,title=title,content=content,draft=True)
                article.save()
                
            article_tag=Article_tag(article=article,article_tag=tag)
            article_tag.save()
            return render(request,"article.html")  
        else:
            if 'publish' in request.POST:
                article=Article(id=id,user_id=user_id,title=title,content=content)
                article.save()
            else:
                article=Article(id=id,user_id=user_id,title=title,content=content,draft=True)
                article.save()
            article_tag=Article_tag(id=id,article=article,article_tag=tag)
            article_tag.save()
            return render(request,"article.html")
    else:
        if id==None:
            user_id  = request.user.id
            article_data=Article_tag.objects.filter(article__draft=True,article__user__id=user_id).values("id","article__id","article__user__first_name","article__title","article__content","article_tag","article__date")
            return render(request,"draft.html",{'article_data':article_data})
        else:    
            draft_data = Article_tag.objects.filter(id=id).values("id","article__id","article__title","article__content","article_tag")
            return render(request,"article.html",{'draft_data':draft_data})
    
        
        
    
def article_list(request,tag_name=None):
    if tag_name==None:
        article_data=Article_tag.objects.filter(article__draft=False).values("article_id","article__user__first_name","article__title","article__content","article_tag","article__date")
        
        all_tags = []
        tag_split={}
        for q in article_data:
            all_tags+= q["article_tag"].split(",")
            tag_id=q["article_id"]
            tag_split[tag_id]=q["article_tag"].split(",")

        tag = Tag.objects.filter(tag_name__in=all_tags).values('tag_name')
        

        tags={}
        for i in tag:
            tag_na=i["tag_name"]
            tag_count=all_tags.count(tag_na)
            tags[tag_na]=tag_count

        paginator = Paginator(article_data, 5)
        page_number = request.GET.get('page')
        article_data = paginator.get_page(page_number)        
        
            
        return render(request,"articles.html",{'article_data':article_data,'tags':tags,'tag_split':tag_split})
    else:
        article_data=Article_tag.objects.filter(article__draft=False,article_tag__contains=tag_name).values("article_id","article__user__first_name","article__title","article__content","article_tag","article__date")
    
        tag_split={}
        for i in article_data:
            tag_name=i["article_tag"].split(",")
            tag_id=i["article_id"]
            tag_split[tag_id]=tag_name
        
        return render(request,"articles.html",{'article_data':article_data,'tag_split':tag_split})
    

def draft_delete(request,id):
    article_data = Article.objects.filter(id=id)
    article_data.delete()
    return redirect("/article_draft")


def user_registration(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        try:
            User.objects.get(username=user_name)
            
            return render(request,'user_registration.html',{'username_error':'Username Already Exists.'})
        except User.DoesNotExist:
            User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=password)
            return redirect('/user_login')
    else:
        return render(request,'user_registration.html')

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=user_name, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
    else:
        return render(request,'user_login.html')
        

def user_logout(request):
    auth.logout(request)
    return redirect('user_login')
    
   
