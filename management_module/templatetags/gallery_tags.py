from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def mantener_params(context, **extra):
    params = {}
    for key in ('q', 'lugar', 'coleccion', 'page'):
        val = context['request'].GET.get(key)
        if val:
            params[key] = val
    params.update(extra)
    if 'page' in params and not params['page']:
        del params['page']
    qs = '&'.join(f'{k}={v}' for k, v in params.items())
    return f'?{qs}' if qs else ''
