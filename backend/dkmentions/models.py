from django.db import models


class FacebookPost(models.Model):

    page_id = models.CharField(max_length=100, default='', null=True)
    post_id = models.CharField(max_length=100, default='', null=True)
    username = models.CharField(max_length=100, default='', null=True)
    content = models.TextField(default='', null=True)

    def __str__(self):
        if self.post_id:
            return self.post_id
        return 'FacebookPost Instance (pk: %d)' % self.pk
    
    def __repr__(self):
        return self.__str__()  # str(self)
