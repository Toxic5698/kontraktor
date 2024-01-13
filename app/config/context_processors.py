import os


def export_vars(request):
    data = {'main_logo': os.getenv("MAIN_LOGO")}
    return data
