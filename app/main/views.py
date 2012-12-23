from app.main.decorators import render_to


@render_to('index.html')
def index(request):
    pass
