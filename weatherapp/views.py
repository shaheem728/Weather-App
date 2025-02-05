from django.shortcuts import render
from django.conf import settings
import datetime
import requests

# Create your views here.
WEATHER_API_KEY = settings.WEATHER_API_KEY
GOOGLE_API_KEY = settings.GOOGLE_API_KEY
SEARCH_ENGINE_ID = settings.SEARCH_ENGINE_ID

def index(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    PARAMS = {'units': 'metric'}
    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1)* 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items")
    try:
        if search_items and len(search_items) > 0:
            image_url = search_items[1]['link']
        else:
            image_url = None  # Fallback in case no images are found
        data = requests.get(url, PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()
        context = {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'image_url':image_url
        }
        return render(request, 'index.html', context)
    except:
        context = {
        'error_message': "Sorry, we couldn't fetch the weather data at this time. Please try again later.",
        'city': city,
        'day': datetime.date.today()
        }
        return render(request, 'index.html', context)
