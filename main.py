import os
import requests
from datetime import datetime, timezone, timedelta

APP_ID = os.environ['nutritionix_APP_ID']
API_KEY = os.environ['nutritionix_API_KEY']
EXERCISE_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'
nutritionix_HEADERS = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    'x-remote-user-id': '0',
}
nutritionix_parameters = {
    'query': input('Tell me which exercises you did: '),  # ran 5k and cycled 20 min
    'gender': 'male',
    'weight_kg': '54.3',
    'height_cm': '170.2',
    'age': '18',
}
exercise_response = requests.post(url=EXERCISE_ENDPOINT, headers=nutritionix_HEADERS, json=nutritionix_parameters)
exercise_data: dict[str: list[dict]] = exercise_response.json()
list_of_exercises: list[dict] = exercise_data['exercises']


SHEETY_AUTH_TOKEN = os.environ['SHEETY_AUTH_TOKEN']
SHEETY_ENDPOINT = os.environ['SHEETY_ENDPOINT']
authorization = {'Authorization': f'Bearer {SHEETY_AUTH_TOKEN}'}

time_diff = timedelta(hours=-7)
my_timezone = timezone(offset=time_diff)
today = datetime.now(tz=my_timezone)
date = today.strftime('%m/%d/%Y')
time = today.strftime('%X')

for exercise in list_of_exercises:
    sheety_HEADERS = {
        'workout': {
            'date': date,
            'time': time,
            'exercise': exercise['name'].title(),
            'duration': str(exercise['duration_min']),
            'calories': str(exercise['nf_calories']),
        }
    }
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_HEADERS, headers=authorization)
