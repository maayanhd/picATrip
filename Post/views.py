from django.views.generic import ListView
from commenting_system.forms import CommentForm
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required


class PostListView(ListView):
    model = Post
    template_name = 'Post/postList.html'
    context_object_name = 'posts'


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # Using only the last 5 (approved) comments (at most- if exist)
    comments = post.comments.filter(active=True).order_by("-created_on")[:5]
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current User to the comment
            new_comment.user = request.user
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'Post/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'label_to_badge_type': {"Recommended": "bg-success",
                                                                             "Quiet": "bg-secondary",
                                                                             "Crowded": "bg-warning",
                                                                             "Chance to meet": "bg-primary",
                                                                             "Want to go": "bg-info"}
                                                     })