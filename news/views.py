from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Rating, Theme
from django.utils import timezone
from .forms import PostForm, RatingForm, ThemeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from math import sqrt,pow

# Create your views here.
def mainpage(request):
    return render(request, 'registration/mainpage.html', {})

def practice(request, Loginf):
    return render(request, 'news/parctice.html', {'Loginf':Loginf})

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'registration/login.html', {'error':'username or password is incorrect'})
    return render(request, 'registration/login.html')

def register(request):
    if request.method == "POST":  # 무언가 받아왔을때
        try :
            user = User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
            auth.login(request, user)
            return redirect('post_list')
        except:
            error = "id is already exist"
            return render(request, 'registration/register.html', {'error':error})

    return render(request, 'registration/register.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('mainpage')

@login_required
def post_list(request):

    recommands_pk_list = []
    recommands_pk_list_prefer = []
    recommands_pk_list_disprefer = []
    controversial_pk_list = []
    print(Post.objects.count())
    if Post.objects.count() != 0 :
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        main_themes = Theme.objects.filter(theme_type='MT')
        sub_themes = Theme.objects.filter(theme_type='ST')
        recommands, controversials = rating_expectation(request)
        if len(recommands) != 0:
            for i in recommands:
                recommands_pk_list.append(i[1])
            if len(recommands_pk_list) > 3:
                recommands_pk_list_prefer = recommands_pk_list[2:]
                recommands_pk_list_disprefer = recommands_pk_list[:2]
            else:
                recommands_pk_list_prefer = recommands_pk_list[2:]
                recommands_pk_list_disprefer = []

        if len(controversials) != 0:
            for i in controversials:
                controversial_pk_list.append(i[0])
        return render(request, 'news/post_list.html', {'posts':posts,'main_themes':main_themes, 'sub_themes':sub_themes,
                                                       'recommands_prefer':recommands_pk_list_prefer,
                                                       'recommands_disprefer':recommands_pk_list_disprefer,
                                                       'recommands_controversial':controversial_pk_list})
    else:
        return render(request, 'news/post_list.html', {'posts':[],'main_themes':[], 'sub_themes':[],
                                                       'recommands_prefer':recommands_pk_list_prefer,
                                                       'recommands_disprefer':recommands_pk_list_disprefer,
                                                       'recommands_controversial':controversial_pk_list})
@login_required
def post_list_theme(request, theme='All'):
    print("theme : ",theme, type(theme))
    #theme에 포함된 글만 보여주는 것
    recommands_pk_list = []
    recommands_pk_list_prefer = []
    recommands_pk_list_disprefer = []
    controversial_pk_list = []
    
    if Theme.objects.count() == 0:
        #Theme이나 post가 없거나, theme을 받아온 경우가 아니라면
        print("theme 0")
        return render(request, 'news/post_list.html',
                      {'posts': [], 'main_themes': [], 'sub_themes':[],
                       'recommands_prefer': recommands_pk_list_prefer,
                       'recommands_disprefer': recommands_pk_list_disprefer,
                       'recommands_controversial': controversial_pk_list}
                      )
    elif Post.objects.count() == 0:
        print("post 0")
        main_themes = Theme.objects.filter(theme_type='MT')
        sub_themes = Theme.objects.filter(theme_type='ST')
        return render(request, 'news/post_list.html',
                      {'posts': [], 'main_themes': main_themes, 'sub_themes': sub_themes,
                       'recommands_prefer': recommands_pk_list_prefer,
                       'recommands_disprefer': recommands_pk_list_disprefer,
                       'recommands_controversial': controversial_pk_list}
                      )
    elif theme=='All':
        print("theme not 0, post not 0")
        posts = Post.objects.all().order_by('-published_date')
        main_themes = Theme.objects.filter(theme_type='MT')
        sub_themes = Theme.objects.filter(theme_type='ST')
        recommands, controversials = rating_expectation(request)
        if len(recommands) != 0:
            for i in recommands:
                recommands_pk_list.append(i[1])
            if len(recommands_pk_list) > 3:
                recommands_pk_list_prefer = recommands_pk_list[2:]
                recommands_pk_list_disprefer = recommands_pk_list[:2]
            else:
                recommands_pk_list_prefer = recommands_pk_list[2:]
                recommands_pk_list_disprefer = []

        if len(controversials) != 0:
            for i in controversials:
                controversial_pk_list.append(i[0])
        return render(request, 'news/post_list.html',
                      {'posts': posts, 'main_themes': main_themes, 'sub_themes': sub_themes,
                       'recommands_prefer': recommands_pk_list_prefer,
                       'recommands_disprefer': recommands_pk_list_disprefer,
                       'recommands_controversial': controversial_pk_list})
    else:
        #theme이 All이 아닐 경우
        theme_obj = Theme.objects.get(theme_title = theme)
        posts = []
        main_themes = Theme.objects.filter(theme_type='MT')
        sub_themes = Theme.objects.filter(theme_type='ST')
        if Post.objects.filter(theme=theme_obj).count() != 0:
            posts = Post.objects.filter(theme=theme_obj).order_by('-published_date')
        recommands, controversials = rating_expectation(request)
        if len(recommands) != 0:
            for i in recommands:
                recommands_pk_list.append(i[1])
            if len(recommands_pk_list) > 3:
                recommands_pk_list_prefer = recommands_pk_list[2:]
                recommands_pk_list_disprefer = recommands_pk_list[:2]
            else:
                recommands_pk_list_prefer = recommands_pk_list[2:]
                recommands_pk_list_disprefer = []

        if len(controversials) != 0:
            for i in controversials:
                controversial_pk_list.append(i[0])
        return render(request, 'news/post_list.html',
                          {'posts': posts, 'main_themes': main_themes, 'sub_themes':sub_themes,
                           'recommands_prefer': recommands_pk_list_prefer,
                           'recommands_disprefer': recommands_pk_list_disprefer,
                           'recommands_controversial': controversial_pk_list})
    


@login_required
def post_practice(request):
    now_user = request.user
    return render(request, 'news/practice.html', {'now_user':now_user})

@login_required
def rating_expectation(request):

    users = User.objects.filter()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')  # 전체 posts
    critics={}
    posts_grade = {}
    for i in users:
        critics[i] ={}
        for j in posts:
            user_post_grade = Rating.objects.filter(rating_user=i,rating_post=j,rating_direct=True) #.get을 썼어도 됬는데.
            if len(user_post_grade) != 0:
                critics[i][j] = user_post_grade[0].rating_grade
                if j in posts_grade: #posts_grade 에 j라는 키가 있다면
                    posts_grade.get(j).append(user_post_grade[0].rating_grade)
                else:
                    temp = []
                    temp.append(user_post_grade[0].rating_grade)
                    posts_grade[j] = temp
    print("critics : " ,critics)
    recomm_list = getRecommendation(critics, users[request.user.pk-1])
    dispersion_list = getDispersion(posts_grade)

    return recomm_list, dispersion_list

def getDispersion(data, index=2):
    li=[]
    new_data= {}

    for i in data:
        vsum = 0
        avg_d = sum(data[i])/len(data[i])
        for j in data[i]:
            vsum = vsum + (j-avg_d)**2
        var = vsum/ len(data[i])
        new_data[i] = var
    li = new_data
    li = sorted(li.items(), key=(lambda x: x[1]), reverse = True)
    return li[:index]

def sim_distance(data, name1, name2):
    sum = 0
    for i in data[name1]:
        if i in data[name2]:  # 같은 영화를 봤다면
            sum += pow(data[name1][i] - data[name2][i], 2)
    return 1 / (1 + sqrt(sum))

def top_match(data, name, index=3, sim_function=sim_distance):
    li = []
    for i in data:
        if name != i:  # 자기 자신은 제외한다
            li.append((sim_function(data, name, i), i))  # 유사도, 이름을 튜플에 묶어 리스트에 추가한다
    # print(li)
    li.sort(key=lambda t: t[0])  # 오름차순 정렬
    li.reverse()  # 내림차순 정렬

    return li

def getRecommendation(data, person, sim_function=sim_distance):
    result = top_match(data, person, len(data))

    simSum = 0  # 유사도 합을 위한 변수
    score = 0  # 평점 합을 위한 변수
    li = []  # 리턴을 위한 리스트
    score_dic = {}  # 유사도 총합을 위한 dic
    sim_dic = {}  # 평점 총합을 위한 dic
    print(result)
    for sim, name in result:  # 튜플이므로 한번에
        if sim < 0: continue  # 유사도가 양수인 사람만
        for food in data[name]:
            if food not in data[person]:  # name이 평가를 내리지 않은 음식
                score += sim * data[name][food]  # 그사람의 음식평점 * 유사도
                score_dic.setdefault(food, 0)  # 기본값 설정
                score_dic[food] += score  # 합계 구함

                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(food, 0)
                sim_dic[food] += sim

            score = 0  # 음식이 바뀌었으니 초기화한다

    for key in score_dic:
        score_dic[key] = score_dic[key] / sim_dic[key]  # 평점 총합/ 유사도 총합
        li.append((score_dic[key], key))  # list((tuple))의 리턴을 위해서.
    li.sort(key=lambda t: t[0])  # 오름차순
    li.reverse()  # 내림차순
    return li


@login_required
def post_detail(request, pk, theme):
    post = get_object_or_404(Post, pk=pk)
    now_user = request.user
    form = RatingForm()
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            Rating.objects.filter(rating_user=now_user,rating_post=post).delete()
            rating.rating_user = now_user
            rating.rating_date = timezone.now()
            rating.rating_post = post
            rating.rating_direct = True
            rating.rating_grade_expect = None
            rating.save()

            print("please")
            rating_expectation(request)

            # rating_expectation(request, post)
            print("post_detail theme", theme)
            return redirect('post_list_theme', theme=theme)
        else :
            rating = Rating.objects.filter(rating_post=post)
            return render(request, 'news/post_detail.html', {'post':post,'rating':rating, 'now_user':now_user, 'form':form})
    else:
        rating = Rating.objects.filter(rating_post=post)
    return render(request, 'news/post_detail.html', {'post':post,'rating':rating, 'now_user':now_user, 'form':form})

@login_required
def post_new(request):
    print("function post_new")
    if request.method == "POST": #무언가 받아왔을때
        form = PostForm(request.POST) #form 형태로 reqest.POST로 받아온 값을 준다.
        if form.is_valid():
            post = form.save(commit=False) #form 형태로 저장하지는 마라, 작성자와 작성시간을 더해야하니깐.
            post.published_date = timezone.now()
            if post.temp_theme != None:
                print("temp_theme == none", post.temp_theme)
                Theme.objects.create(theme_title=post.temp_theme,theme_type='ST')
                post.theme = Theme.objects.get(theme_title = post.temp_theme)
            post.save() #이제 저장해라.
            return redirect('post_detail', theme=post.theme.theme_title,pk=post.pk) #post_detail로 가고, pk=post.pk로 줄께.
    else:
        form = PostForm()
    return render(request, 'news/post_edit.html', {'form':form})

def post_delete(request, theme, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def theme_new(request):
    print("function theme_new")
    if request.method == "POST":  # 무언가 받아왔을때
        form = ThemeForm(request.POST)  # form 형태로 reqest.POST로 받아온 값을 준다.
        if form.is_valid():
            theme = form.save(commit=False)  # form 형태로 저장하지는 마라, 작성자와 작성시간을 더해야하니깐.
            if Theme.objects.filter(theme_title=theme.theme_title).count() == 0:
                theme.save()  # 이제 저장해라.
                return redirect('post_list')
            else:
                error = "already exist theme"
                return render(request, 'news/theme_edit.html', {'form':form,'error':error})
    form = ThemeForm()
    themes = Theme.objects.all()
    print("themes", themes)
    return render(request, 'news/theme_edit.html', {'form': form, 'themes':themes})

def theme_delete(request, theme):
    temp_theme = Theme.objects.get(theme_title=theme)
    temp_theme.delete()
    return redirect('post_list')

def theme_change(request,theme):
    temp_theme = Theme.objects.get(theme_title=theme)
    if temp_theme.theme_type == 'MT':
        temp_theme.theme_type = 'ST'
    else:
        temp_theme.theme_type = 'MT'
    temp_theme.save()
    return redirect('post_list')

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', theme=post.theme.theme_title, pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'news/post_edit.html', {'form': form})