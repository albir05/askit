from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from .models import Question,Comment
from .forms import CommentForm
from django.urls import reverse,reverse_lazy
from simple_search import search_filter
import razorpay
from django.core.mail import send_mail

# Create your views here.
def about(request):
    return render(request,'about.html')
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
         context['errmsg']="Fields cannot be empty"
        elif upass!=ucpass:
            context['errmsg']="Password and Confirm password did not match"
        else: 
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User created successfully"
            except Exception:
                context['errmsg']="User with same name already exist"    
        return render(request,'signup.html',context)
    else:    
        return render(request,'signup.html')  
   

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
      
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            print(u)
            if u is not None:
                login(request,u)
                return redirect('/')
            else:
                context['errmsg']="Invalid Username and Password"
                return render(request,'login.html',context)    
               
    else:
        return render(request,'login.html') 
  
def user_logout(request):
    logout(request)
    return redirect('/')  

def like_view(request,pk):
    post = get_object_or_404(Question,id=request.POST.get('question_id'))
    liked = False
    if post.likes.filter(id= request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('askit_app:question-detail',args=[str(pk)]))            

#crud     function

class QuestionListView(ListView):
    model=Question
    context_object_name = 'questions'
    ordering = ['-date_created']

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     search_input = self.request.GET.get('search-area') or ""
    #     if search_input:
    #         context['questions'] = context['questions'].filter(title)
    #         context['search_input'] = search_input
    #         return context

class QuestionDetailView(DetailView):
    model=Question

    def get_context_data(self,*args,**kwargs):
        context = super(QuestionDetailView,self).get_context_data()
        something = get_object_or_404(Question, id=self.kwargs['pk'])
        total_likes = something.total_likes()
        liked = False
        if something.likes.filter(id=self.request.user.id).exists():
            liked=True

        context['total_likes']=total_likes
        context['liked']=liked
        return context


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model=Question  
    fields = ['title','content']  

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model=Question  
    fields = ['title','content']  

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)    

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        else:
            return False

class QuestionDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model=Question 
    context_object_name = 'question'
    success_url = "/"
    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        else:
            return False 

class CommentDetailView(CreateView):
    model=Comment
    form_class = CommentForm
    template_name = 'askit_app/question_detail.html'

    def form_valid(self,form):
        form.instance.question_id = self.kwargs['pk']            
        return super().form_valid(form)
    success_url = reverse_lazy('askit_app:question-detail')

class AddCommentView(CreateView):
    model=Comment
    form_class = CommentForm
    template_name = 'askit_app/question_answer.html'    
    
    def form_valid(self,form):
        form.instance.question_id = self.kwargs['pk']            
        return super().form_valid(form)
    success_url = reverse_lazy('askit_app:question-list')

    #######################################################
def pricing(request):
    return render(request,'pricing.html')    
    
def makepayment(request):
    
    client = razorpay.Client(auth=("rzp_test_pjmfONoAV5hhRJ", "2qLFlWxOv0vaA1jxWEEHwbcA"))
    data = { "amount": 100000, "currency": "INR" }
    payment = client.order.create(data=data)
    #print(payment)
    username=request.user.username
    print(username)
    context={}
    context['data']=payment
    context['username']=username
    return render(request,'products.html',context)

def sendusermail(request,username):
    #we cant access email directly here so we have to pass from above function
    msg="Order details are:......"
    send_mail(
        "Ekart order placed successfully!!",
        msg,
        "kauralbir@gmail.com",
        [username],
        fail_silently=False,
    )
    return HttpResponse("Mail sent successfully")
            