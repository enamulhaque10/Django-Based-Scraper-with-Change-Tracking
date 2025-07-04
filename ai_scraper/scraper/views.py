
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import ScrapedItem, ChangeLog
#from .tasks import scrape_fbi_data


@login_required
def home(request):
    items = ScrapedItem.objects.all().order_by('-timestamp')
    return render(request, 'scraper/home.html', {'items': items})


@login_required
def search_items(request):
    query = request.GET.get('search', '')
    items = ScrapedItem.objects.filter(title__icontains=query).order_by('-timestamp')
    return render(request, 'scraper/partials/item_list.html', {'items': items})


@login_required
def show_change_log(request):
    changes = ChangeLog.objects.all().order_by('-timestamp')[:20]
    html = render_to_string('scraper/partials/change_log_modal.html', {'changes': changes})
    return HttpResponse(html)


# @login_required
# def trigger_scrape(request):
#     scrape_fbi_data.delay()
#     return JsonResponse({'message': 'Scrape started'})
