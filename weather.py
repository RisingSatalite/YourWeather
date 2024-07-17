import requests
import json
import geocoder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from dotenv import load_dotenv
import os

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text=self.data))
        layout.add_widget(Label(text=f'Tempurature {self.tem}'))
        layout.add_widget(Label(text=f'Weather is {self.des}'))
        layout.add_widget(Label(text=f'Tempurature fells like {self.feel}'))
        layout.add_widget(Label(text=f'Expected high {self.high}'))
        layout.add_widget(Label(text=f'Expected low {self.low}'))
        layout.add_widget(Label(text=f'Humidity {self.humidity}'))

        return layout
    
    def set_data(self, text):
        self.data = text
    
    def set_weather_data(self, tem, des, feel, high, low, humidity):
        self.tem = tem
        self.des = des
        self.feel = feel
        self.high = high
        self.low = low
        self.humidity = humidity

    def set_cooredinates(self, latitude, longitude):
        self.lat = latitude
        self.long = longitude

if __name__ == '__main__':
    g = geocoder.ip('me')

    # Extract latitude and longitude
    latitude = g.latlng[0]
    longitude = g.latlng[1]

    #print(latitude)
    #print(longitude)

    # Replace 'your_api_key' with your actual API key from OpenWeatherMap
    load_dotenv()
    api_key = os.getenv('api_key')
    city = 'London'
    call_type_id = f'id={city}'
    call_type = f'q={city}'
    call_type_ll = f'lat={latitude}&lon={longitude}'
    url = f'http://api.openweathermap.org/data/2.5/forecast?{call_type_ll}&appid={api_key}'

    x = requests.get(url)

    data = json.loads(x.text)

    # Accessing specific information, for example, temperature and weather description of the 4th forecast entry
    entry = data['list'][3]
    temperature = entry['main']['temp']
    weather_description = entry['weather'][0]['description']

    #print(f"Temperature: {temperature}")
    #print(f"Weather Description: {weather_description}")

    app = MyApp()
    app.set_data('Your Weather')
    app.set_weather_data(str(temperature), str(weather_description), str(entry['main']['feels_like']), str(entry['main']['temp_max']), str(entry['main']['temp_min']), str(entry['main']['humidity']))
    app.run()
