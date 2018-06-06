import django
def getlang(request):
    """return the current selected language"""
    return {
        'lang': request.LANGUAGE_CODE
    }