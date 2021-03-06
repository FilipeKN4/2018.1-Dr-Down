from ..models.model_commentary import Commentary
from ..models.model_post import Post
from .view_base import BaseViewTemplate
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from drdown.forum.form.forum_forms import ComentaryForm


class CommentaryListView(BaseViewTemplate, ListView):
    model = Commentary

    def get_context_data(self, **kwargs):
        context = super(CommentaryListView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs.get('post_pk'))
        return context

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs.get('post_pk'))
        queryset = Commentary.objects.filter(post=post)
        return queryset


class CommentaryCreateView(BaseViewTemplate, CreateView):
    model = Commentary
    template_name = 'forum/form_commentary.html'
    form_class = ComentaryForm

    def get_success_url(self, **kwargs):
        success_create_url = reverse_lazy(
            viewname='forum:list_commentary',
            kwargs={
                'pk': self.kwargs.get('pk'),
                'post_pk': self.kwargs.get('post_pk'),
                'slug': self.kwargs.get('slug')
            }
        )

        return success_create_url

    def get_context_data(self, **kwargs):
        context = super(CommentaryCreateView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs.get('post_pk'))
        return context

    def form_valid(self, form):
        # Get post that commentary belongs to
        form.instance.post = Post.objects.get(pk=self.kwargs.get('post_pk'))
        form.instance.created_by = self.request.user
        form.save()

        return super(CommentaryCreateView, self).form_valid(form)


class CommentaryDeleteView (BaseViewTemplate, DeleteView):
    model = Commentary
    success_url = reverse_lazy('forum:list_categories')

    def get_object(self):
        commentary = Commentary.objects.get(
            pk=self.kwargs.get('commentary_pk')
        )
        return commentary

    def get_success_url(self, **kwargs):
        success_delete_url = reverse_lazy(
            viewname='forum:list_commentary',
            kwargs={
                'pk': self.kwargs.get('pk'),
                'post_pk': self.kwargs.get('post_pk'),
                'slug': self.kwargs.get('slug')
            }
        )

        return success_delete_url


class CommentaryUpdateView(BaseViewTemplate, UpdateView):
    model = Commentary
    template_name = 'forum/form_commentary.html'
    fields = ['message']
    success_url = reverse_lazy('forum:list_categories')

    def get_success_url(self, **kwargs):
        success_update_url = reverse_lazy(
            viewname='forum:list_commentary',
            kwargs={
                'pk': self.kwargs.get('pk'),
                'post_pk': self.kwargs.get('post_pk'),
                'slug': self.kwargs.get('slug')
            }
        )

        return success_update_url

    def get_context_data(self, **kwargs):
        context = super(CommentaryUpdateView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs.get('post_pk'))
        return context

    def get_object(self):
        commentary = Commentary.objects.get(
            pk=self.kwargs.get('commentary_pk')
        )
        return commentary

    def form_valid(self, form):
        # Get updated_at datetime
        form.instance.updated_at = timezone.now()
        form.save()

        return super(CommentaryUpdateView, self).form_valid(form)
