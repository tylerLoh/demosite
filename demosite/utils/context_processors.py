""" To register context processor function to templates engine

More information about this page, see
https://docs.djangoproject.com/en/dev/ref/templates/api/
"""
from datetime import datetime


def template_variable(request):
    """

    Parameters
    ----------
    request : HttpRequest object
        Object of HttpRequest
    Returns
    -------
    dict
        A dict of key value used for template
    """

    context_extras = {'year': datetime.now().year,
                      'month': datetime.now().month,
                      'date': 123}
    return context_extras
