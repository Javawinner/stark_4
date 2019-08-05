from stark.service.v1 import site
from app02 import models
from stark.service.v1 import StarkHandler


class HostHandler(StarkHandler):
    list_display = ['host', 'ip']


class RoleHandler(StarkHandler):
    list_display = ['id', 'title']


class ProjectHandler(StarkHandler):
    list_display = ['id', 'title']


site.register(models.Host, HostHandler)
site.register(models.Role,RoleHandler)
site.register(models.Project,ProjectHandler)
