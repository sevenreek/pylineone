from django import template

register = template.Library()

STATUS_COLORS = {
    'new' : 'info',
    'attempted': 'warning',
    'solved': 'success'
}

@register.simple_tag(takes_context=True)
def get_task_status(context, task_id):
    request = context['request']
    status = request.COOKIES.get(f"task{task_id}", "new")
    return status.upper()

@register.simple_tag(takes_context=True)
def get_task_status_color(context, task_id):
    request = context['request']
    status = request.COOKIES.get(f"task{task_id}", "new")
    return STATUS_COLORS[status]

@register.simple_tag(takes_context=True)
def get_task_last_attempt(context, task_id):
    print(f"Trying to get attempt of {task_id}")
    request = context['request']
    attempt = request.COOKIES.get(f"task{task_id}_attempt", "None # write your code here")
    print(f"Attempt is {attempt}")
    return attempt


