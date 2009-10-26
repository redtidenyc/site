from rt_www.index.models import Blog

class Service:
    def get_blog(self, bid):
        b = Blog.objects.get(pk=bid)
        return { 'title':b.title, 'id':b.id, 'author':'%s' %(b.author), 'pub_date':'%s' %(b.pub_date) }

service = Service()
