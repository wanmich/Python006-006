from django.shortcuts import render
from .models import ShortComments


# Create your views here.

def show_short_comments(request):
    q = request.GET.get('q')
    print(f"q: {q}")
    if q:
        q_key_words = [i.strip() for i in q.split(' ')]
        pattern = ""
        for word in q_key_words:
            pattern += fr'{word}|'
        pattern = pattern.rstrip('|')
        results = ShortComments.objects.filter(stars__gt=3, comment__regex=pattern)
        q_words = ' '.join(q_key_words)
    else:
        results = ShortComments.objects.filter(stars__gt=3)
        q_words = None
    count = results.count()
    return render(request, 'index.html', locals())
