from django.template import Library
from rt_www.admin.templatetags.admin_list import result_list, pagination

register = Library()

pagination = register.inclusion_tag('admin/pagination.html')(pagination)
result_list = register.inclusion_tag('admin/change_list_results.html')(result_list)
