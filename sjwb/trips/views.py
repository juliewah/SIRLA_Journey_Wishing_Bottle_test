from django.shortcuts import render, redirect, get_object_or_404
#建立首頁
from trips.models import Post, Comment
from .forms import PostForm, post_comment_form
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

def home(request):
	post_list = Post.objects.all()
	return render(request, 'home.html', {
		'post_list': post_list,
		})

def attraction(request):
	post = Post.objects.all()
	art_comment = []
	for po in post:
		if po.comment_set.all():
			art_comment.append(po.comment_set.all())
		else:
			art_comment.append([])
	post_list = zip(post, art_comment)
	comment_form = post_comment_form()
	return render(request, 'attraction.html', {
		'post_list': post_list,
		})

def accomodation(request):
	post = Post.objects.all()
	art_comment = []
	for po in post:
		if po.comment_set.all():
			art_comment.append(po.comment_set.all())
		else:
			art_comment.append([])
	post_list = zip(post, art_comment)
	comment_form = post_comment_form()
	return render(request, 'accomodation.html', {
		'post_list': post_list,
		})

def restaurant(request):
	post = Post.objects.all()
	art_comment = []
	for po in post:
		if po.comment_set.all():
			art_comment.append(po.comment_set.all())
		else:
			art_comment.append([])
	post_list = zip(post, art_comment)
	comment_form = post_comment_form()
	return render(request, 'restaurant.html', {
		'post_list': post_list,
		})

def post_detail(request, pk):
	post = Post.objects.get(pk=pk)
	return render(request, 'post.html', {'post':post})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'post_edit.html', {'form':form})

def post_delete(request, pk):
	post = Post.objects.get(pk=pk)
	post.delete()
	return redirect('/')

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST,request.FILES, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, '/home/', {'form': form})

def login(request):
	if request.user.is_authenticated:
		return redirect('/home/')
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username = username, password = password)
	if user is not None and user.is_active:
		auth.login(request, user)
		return redirect('/home/')
	else:
		return render(request, 'login.html', locals())

def logout(request):
	auth.logout(request)
	return redirect('/home/')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		print("Errors", form.errors)
		if form.is_valid():
			form.save()
			return redirect('/')
		else:
			return render(request, 'registration/register.html', {'form':form})
	else:
		form = UserCreationForm()
		context = {'form':form}
		return render(request, 'registration/register.html', context)

def Like(request, pk):
	post = get_object_or_404(Post, pk=pk)
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True
	return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

def post_new_comment(request, post_id): 
	the_post = Post.objects.get(pk=post_id)
	if request.method =="POST":
		comment_form = post_comment_form(request.POST or None)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.comment_post = the_post
			new_comment.save()
			messages.success(request, "成功新增留言")
			return redirect('/attraction')
		else:
			return redirect('/attraction')