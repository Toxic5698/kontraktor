import os


def export_vars(request):
    data = {
        'main_logo': os.getenv("MAIN_LOGO"),
        'css_file': os.getenv("CSS_FILE"),
        'environ': os.getenv("ENVIRONMENT"),
    }
    return data
