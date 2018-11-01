from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """主题数据"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        # print('++++++++++++++++', User.objects.all())
        """返回主题数据"""
        return self.text

class Entry(models.Model):
    """条目数据"""
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
 
    def __str__(self):
        """返回数据"""
        return self.text[:50] + "..."
