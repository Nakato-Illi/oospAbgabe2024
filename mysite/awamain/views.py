from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
# from django.utils.html import strip_tags
import django.utils.html as d
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse

from reportlab.pdfgen import canvas
from django.shortcuts import render

from .models import Post, Category, Comment
from .forms import PostForm, UpdateForm, CommentForm


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


class UserBooksView(ListView):
    model = Post
    template_name = 'user_books.html'
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        liked_posts = self.request.user.book_post.all()
        context = super(UserBooksView, self).get_context_data(*args, **kwargs)
        context['liked_posts'] = liked_posts
        context['cat_menu'] = cat_menu
        return context


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    catlist = Category.objects.filter(id=cats)
    category = catlist[0] if len(catlist) > 0 else 'unknown'
    return render(request, 'categories.html',
                  context={'cats': cats.title(), 'category_posts': category_posts, 'category': category})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('book-detail', args=[str(pk)]))


class BookDetailView(DetailView):
    model = Post
    template_name = 'book_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)

        data = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = data.total_likes()

        liked = False
        if data.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'pdf' in self.request.GET:
            pdf_content = self.generate_pdf(context)
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'filename="{context["post"].title}.pdf"'
            return response
        else:
            return super().render_to_response(context, **response_kwargs)

    def generate_pdf(self, context):
        from io import BytesIO

        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Create a PDF document
        linebreak = '\\Ä;Ä;Ä;Ä;Ä\\'
        start = 80
        book = context.get('post')
        p.drawString(start, 750, f"Book Title - {book.title}")

        y = 700
        p.drawString(start, y - 20, f"Author: {book.author}")
        p.drawString(start, y - 40, f"Published: {book.pub_date}")
        stripped_body = d.strip_tags(book.body)
        stripped_body = stripped_body.replace('\n', linebreak)
        sy = y - 80
        split = stripped_body.split()

        parsed = []
        tmp_string = ''
        tmp_list = []
        for i in range(len(split)):
            string = split[i]

            if string == linebreak or len(tmp_string + string) > 70:
                parsed.append(' '.join(tmp_list))
                tmp_string = string.replace(linebreak, '')
                tmp_list = [tmp_string]
            else:
                tmp_string += string
                tmp_list.append(string)

        parsed.append(' '.join(tmp_list))

        for i in range(len(parsed)):
            string = parsed[i]
            if i == 0:
                p.drawString(start, sy, f"Book data: {string}")
            else:
                if linebreak in string:
                    sy -= 20
                    string = string.replace(linebreak, '')
                p.drawString(start, sy, f"{string}")
            if sy - 20 <= 80 and i < len(parsed)-2:
                p.showPage()
                sy = 750
            else:
                sy -= 20

        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer.getvalue()


class AddBookView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_book.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.kwargs['pk']})


class UpdateBookView(UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'update_book.html'


class DeleteBookView(DeleteView):
    model = Post
    template_name = 'delete_book.html'
    success_url = reverse_lazy('home')
