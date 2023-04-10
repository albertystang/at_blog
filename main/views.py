from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Blog, BlogComment
from .forms import ContactForm, CreateBlogForm, CommentBlogForm


""" def blog_home(request):
    blogs = Blog.objects.all().order_by('-post_date')[:10]
    context = {'blogs': blogs}
    return render(request, 'main/blog_home.html', context)
 """


class blog_home(generic.ListView):
    model = Blog
    template_name = 'main/blog_home.html'


#@login_required(login_url='login')
def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    blogs = Blog.objects.all().order_by('-post_date')[:10]
    comments = BlogComment.objects.filter(blog=blog.id, )
    form = CommentBlogForm()
    if request.method == 'POST':
        form = CommentBlogForm(request.POST or None)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.blog = blog
            comment_form.author = request.user
            comment_form.save()
            messages.success(request, 'Your comment has been posted...')            
        else:
            messages.error(request, 'An error in creating your comment...')
        return redirect('blog_detail', blog.slug)
    comments = blog.blogcomments.all()
    context = {'blog': blog, 'blogs': blogs, 'form': form, 'comments': comments}
    return render(request, 'main/blog_detail.html', context)


""" class blog_detail(generic.DetailView):
    model = Blog
    template_name = 'main/blog_detail.html' """


""" def contact_us(request):
    form = ContactForm()    
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():       
            form.save()            
            messages.success(request, 'Your form is submitted successfully...')
            return redirect('home')
        else:            
            messages.success(request, 'Please fill the form properly...')
    context = {'form': form}
    return render(request, 'main/contact_us.html', context) """


class contact_us(SuccessMessageMixin, generic.CreateView):
    form_class = ContactForm
    template_name = 'main/contact_us.html'
    success_url = reverse_lazy('home')
    success_message = 'Your query has been submitted, we will contact you soon...'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please submit the form again...")
        return redirect('home')
    

@login_required(login_url='login')
def CreateBlog(request):
    form = CreateBlogForm()
    if request.method == 'POST':
        form = CreateBlogForm(request.POST or None)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Your blog has been created...')                       
        else:
            messages.error(request, 'An error in creating the blog, please try again...')
        return redirect('home')            
    return render(request, 'main/create_blog.html', {'form': form})


""" class CreateBlog(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    login_url = 'login'
    form_class = CreateBlogForm
    template_name = 'main/create_blog.html'
    success_url = reverse_lazy('home')
    success_message = 'Your blog has been created...' """


@login_required
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    form = CreateBlogForm(instance=blog)    
    if request.method == 'POST':
        form = CreateBlogForm(request.POST or None, instance=blog)
        if form.is_valid():
            """ updated_form = form.save(commit=False)
            updated_form.author = request.user
            updated_form.save() """
            form.save()
            messages.success(request, 'Your blog has been updated...')
            return redirect('blog_detail', blog.slug)
        else:
            messages.success(request, 'An error in updating...')
    return render(request, 'main/update_blog.html', {'form': form})


""" class UpdateBlogView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = CreateBlogForm
    model = Blog
    template_name = 'main/update_blog.html'
    login_url = 'login'
    success_url = reverse_lazy('home')
    success_message = 'Your blog has been successfully created...' """


class DeleteBlogView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Blog
    template_name = 'main/delete_blog.html'
    login_url = 'login'
    success_url = reverse_lazy('home')
    success_message = 'Your blog has been sucessfully deleted...'
