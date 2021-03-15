from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from django.utils import timezone
from  .forms import PostFrom


def index(request):
    return render(request,'post_list.html')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # posts = Post.objects.order_by('Created_date')
    # return render (request,'post_list.html',{'posts':posts})
    return render(request, 'post_data/post_list.html', {'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render (request,'post_data/post_detail.html',{'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostFrom(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostFrom()
    return render(request,'post_data/post_edit.html',{'form':form})

def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method =="POST":
        form = PostFrom(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date= timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostFrom(instance=post)
    return render(request, 'post_data/post_edit.html', {'form': form})

def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('new')
    # return render(request, 'post_data/post_list.html')
