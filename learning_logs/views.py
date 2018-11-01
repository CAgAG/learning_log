from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry
from .forms import TopicForm,EntryForm

def index(request):
    """learning_log 主页"""
    context = {'user': request.user}
    return render(request, 'learning_logs/index.html', context)

@login_required
def topics(request):
    """主题集"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """单个主题显示,及对应条目"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries, 'topic_id': topic_id}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """加入新条目"""
    if request.method != 'POST':
        # 没有数据则创建新表单
        form = TopicForm()
    else:
        # POST提交数据及处理数据
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    # print('new_entry Start')
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    # if topic.owner != request.user:
    #     raise Http404
    # print('topic get')
    if request.method != 'POST':
        # 没有数据则创建新表单
        form = EntryForm()
        # print('get a new form')
    else:
        # POST提交数据及处理数据.
        form = EntryForm(data=request.POST)
        # print('start form')
        # print('>>>>>>>>>', request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                    args=[topic_id]))

    context = {'topic': topic, 'form': form, 'topic_id': topic_id}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑一个已存在的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST提交数据及处理数据
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form, 'topic_id': topic.id, 'entry_id': entry_id}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def del_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    topic.delete()
    return HttpResponseRedirect(reverse('learning_logs:topics'))

@login_required
def del_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    entry.delete()
    return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

@login_required
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != "POST":
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'topic': topic, 'topic_id': topic_id, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)



