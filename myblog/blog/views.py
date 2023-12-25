from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import *
from .forms import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 10
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().order_by('-date')
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['comment_form'] = CommentForm()
        context['comment_comment_form'] = CommentCommentForm()
        return context


class Login(LoginView):
    template_name = 'blog/login.html'


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = User.objects.get(pk=self.kwargs.get('pk'))
        user_posted = UserPosted.objects.filter(user=self.kwargs.get('pk')).values_list('post', flat=True)
        posts = Post.objects.filter(pk__in=user_posted)
        user_commented = Comment.objects.filter(post_id__in=posts.values_list('id', flat=True))

        context['user_commented'] = user_commented
        context['profile'] = profile
        context['posts'] = posts
        context['post_form'] = PostForm()
        context['comment_form'] = CommentForm()
        context['comment_comment_form'] = CommentCommentForm()
        return context


def delete(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect(reverse('home'))


class UserView(UpdateView):
    template_name = 'blog/update.html'
    model = User
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save()
        update_session_auth_hash(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        user_posted = UserPosted.objects.create(post=post, user=self.request.user)
        user_posted.save()

        return redirect(reverse('profile', kwargs={'pk': self.request.user.pk}))


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs['post_id']
        comment.user = self.request.user
        comment.save()
        if 'profile_id' in self.kwargs:
            return redirect(reverse('profile', kwargs={'pk': self.kwargs['profile_id']}))
        else:
            return redirect('home')


class CommentCommentedView(LoginRequiredMixin, CreateView):
    model = CommentCommented
    form_class = CommentCommentForm

    def form_valid(self, form):
        comment_comment = form.save(commit=False)
        comment_id = self.kwargs['pk']
        comment_comment.comment = Comment.objects.get(id=comment_id)
        comment_comment.user = self.request.user
        comment_comment.save()

        if 'profile_id' in self.kwargs:
            return redirect(reverse('profile', kwargs={'pk': self.kwargs['profile_id']}))
        else:
            return redirect('home')


class CommentUpdate(UpdateView):
    template_name = 'blog/update_comment.html'
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        if 'profile_id' in self.kwargs:
            return reverse('profile', kwargs={'pk': self.kwargs['profile_id']})
        else:
            return reverse('home')


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect(reverse('home'))


class CommentCommentedUpdate(UpdateView):
    template_name = 'blog/comment_commented_update.html'
    model = CommentCommented
    form_class = CommentCommentForm

    def get_success_url(self):
        if 'profile_id' in self.kwargs:
            return reverse('profile', kwargs={'pk': self.kwargs['profile_id']})
        else:
            return reverse('home')


def delete_comment_commented(request, comment_id):
    comment = CommentCommented.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect(reverse('home'))
