# %%
import requests

longitude = -43.222457
latitude = -22.982818

try:
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0'
    }
    #response = requests.get('https://nominatim.openstreetmap.org/reverse?format=xml&lat=52.5487429714954&lon=-1.81602098644987&zoom=18&addressdetails=1')
    response = requests.get(url,headers=headers)
except Exception as e: print(e)
# %%

response.status_code

# %%

response.content

# %%

response.json()

# %%
