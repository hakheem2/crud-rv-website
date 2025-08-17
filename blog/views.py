from django.shortcuts import render

# Create your views here.
def blog(request):
    return render(request, 'blog.html')

def blog_post(request):
    return render(request, 'blog-post.html')