def get_data_in_dict(request):
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    return data
