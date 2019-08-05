from django.conf.urls import url
from django.shortcuts import HttpResponse, render


class StarkHandler(object):
    list_display = []

    def __init__(self, model_class, prev):
        self.model_class = model_class
        self.prev = prev

    def change_list(self, request):
        '''
        查看页面
        :return:
        '''
        model_name = self.model_class._meta.model_name  # 用户要访问的表
        list_display = self.list_display  # 页面要显示的列

        # 处理表头
        header_list = []
        for key in self.list_display:
            verbose_name = self.model_class._meta.get_field(key).verbose_name
            header_list.append(verbose_name)

        # 处理表的内容
        data_list = self.model_class.objects.all()
        body_list = []
        for row in data_list:
            row_list = []
            for key in list_display:
                row_list.append(getattr(row, key))
            body_list.append(row_list)

        print(body_list)

        return render(request, 'stark/changelist.html',
                      {'data_list': data_list,
                       'model_name': model_name,
                       'header_list': header_list,
                       'body_list': body_list})

    def add_view(self, request):
        '''
        添加页面
        :return:
        '''
        return HttpResponse('%s添加页面' % (self.model_class._meta.model_name))

    def change_view(self, request, pk):
        '''
        修改页面
        :return:
        '''
        return HttpResponse('%s修改页面' % (self.model_class._meta.model_name))

    def delete_view(self, request, pk):
        '''
        删除页面
        :return:
        '''
        return HttpResponse('%s删除页面' % (self.model_class._meta.model_name))

    def get_url_name(self, param):
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return '%s_%s_%s_%s' % (app_label, model_name, self.prev, param)
        return '%s_%s_%s' % (app_label, model_name, param)

    @property
    def get_list_url_name(self):
        '''
        获取列表页面的URL的路由别名
        :return:
        '''
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        '''
        获取添加页面的URL的路由别名
        :return:
        '''
        return self.get_url_name('add')

    @property
    def get_change_url_name(self):
        '''
        获取编辑页面的URL的路由别名
        :return:
        '''
        return self.get_url_name('change')

    @property
    def get_delete_url_name(self):
        '''
        获取删除页面的URL的路由别名
        :return:
        '''
        return self.get_url_name('delete')

    @property
    def get_urls(self):
        '''
        准备二级路由分发的url数据
        :return:
        '''

        patterns = []

        patterns.append(url(r'list', self.change_list, name=self.get_list_url_name))
        patterns.append(url(r'add', self.add_view, name=self.get_add_url_name))
        patterns.append(url(r'edit/(\d+)', self.change_view, name=self.get_change_url_name))
        patterns.append(url(r'del/(\d+)', self.delete_view, name=self.get_delete_url_name))

        patterns.extend(self.extra_urls)
        return patterns

    @property
    def extra_urls(self):
        return []


class StarkSite(object):

    def __init__(self):
        self.app_name = 'stark'
        self.namespace = 'stark'
        self._register = []

    def register(self, model_class, handler_class=None, prev=None):
        '''
        操作_register数据
        :param model_class: 数据库表对应models文件中对应的类
        :param handler_class: 处理请求的视图函数所在的类
        :param prev:生成URL的前缀
        :return:
        '''
        if not handler_class:
            handler_class = StarkHandler
        self._register.append(
            {'model_class': model_class, 'handle_class': handler_class(model_class, prev), 'prev': prev})

    @property
    def get_urls(self):
        '''
        准备一级路由分发的url数据和调用二级路由分发的url数据
        :return:
        '''
        patterns = []
        for item in self._register:
            model_class, handle_class, prev = item['model_class'], item['handle_class'], item['prev']
            model_name, app_label = model_class._meta.model_name, model_class._meta.app_label
            if prev:
                patterns.append(url(r'^%s/%s/%s/' % (app_label, model_name, prev), (handle_class.get_urls, None, None)))
            else:
                patterns.append(url(r'^%s/%s/' % (app_label, model_name), (handle_class.get_urls, None, None)))

        return patterns

    @property
    def urls(self):
        return self.get_urls, self.app_name, self.namespace


site = StarkSite()
