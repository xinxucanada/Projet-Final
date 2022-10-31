from django.utils.safestring import mark_safe
from django.http.request import QueryDict
import copy
import hashlib
from django.conf import settings

# Permet de cacher mot de passe dans la base de données
# Prendre de la vidéo https://www.bilibili.com/video/BV1rT4y1v7uQ?p=79&vd_source=63d29f729d495ccb836eeccb160a82dd
# Auteur: Peiqi Wu
# Est utilisé dans la fonction md5()

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


# Permet de séparer les données selon page_size, puis afficher les links des pages
# Prendre de la vidéo https://www.bilibili.com/video/BV1rT4y1v7uQ?p=74&vd_source=63d29f729d495ccb836eeccb160a82dd
# Auteur: Peiqi Wu
# Modifié par Xin pour qu'elle fonnctione pour la liste
# Est utilisé dans la fonction pagination

class Pagination(object):
    
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.page_param = page_param
        self.query_dict = query_dict
    
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
 
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start: self.end]

        
        # total_count = queryset.count() changer la fonction count() à len() pour qu'elle fonction quand l'entree n'est pas un queryset
        total_count = len(queryset)
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):

        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count 
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1 
            elif self.page > self.total_page_count - self.plus:
                end_page = self.total_page_count
                start_page = self.total_page_count - 2 * self.plus
            else:
                start_page = self.page - self.plus
                end_page = self.page + self.plus
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])
        
        page_str_list.append('<li><a href="?{}">&lt;&lt;</a></li>'.format(self.query_dict.urlencode()))
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            prev = '<li><a href="?{}">&lt;</a></li>'.format(self.query_dict.urlencode())
        else:
            prev = '<li><a href="?{}">&lt;</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page+1])
            nextpage = '<li><a href="?{}">&gt;</a></li>'.format(self.query_dict.urlencode())
        else:
            nextpage = '<li><a href="?{}">&gt;</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(nextpage)
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">&gt;&gt;</a></li>'.format(self.query_dict.urlencode()))
        page_string = mark_safe(''.join(page_str_list))

        return page_string