from haystack.forms import ModelSearchForm

def context(request):
    c = {}
    c['searchform'] = ModelSearchForm()

    return c