from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
import requests



class WeatherLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs , orientation = 'vertical')
        self.padding = 50
        self.spacing = 30
        self.welcome = Label(text="Welcome to the simple weather app", font_size = '18' , halign = 'center', valign = 'middle', height = '40',)
        self.City = TextInput(hint_text = 'Which city weather you would  like to check?',size_hint_y = None , height = '50', font_size = '18', halign = 'center' )
        self.City.padding_y = (10, 10)
        self.weatherbutton = Button(text="Check Weather",height = '50' , font_size = '16', size_hint_y = None)
        self.Temp = Label(text='Temp : ')
        self.Type = Label(text='Weather : ')
        self.Humidity = Label(text = 'Humidity : ')
        self.add_widget(self.welcome)
        self.add_widget(self.Temp)
        self.add_widget(self.Humidity)
        self.add_widget(self.Type)
        self.add_widget(self.City)
        self.add_widget(self.weatherbutton)
        self.weatherbutton.bind(on_press = self.WeatherApi)
        

    def coordinates(self, city):
        url = f'https://nominatim.openstreetmap.org/search?city={city}&format=json&limit=1'
        headers = {'User-Agent' : 'SimpleWeatherApp ' }
        response = requests.get(url , headers = headers)

        if response.status_code != 200 : 
            return None, None
        
        success = response.json()
        if  len(success) > 0:
            lat = float(success[0]["lat"])
            lon = float(success[0]["lon"])
            return lat , lon
        else : 
            return None , None

    def WeatherApi(self , instance):
        self.welcome.text = "Welcome to the simple weather app"
        city = self.City.text
        lat , lon = self.coordinates(city)
        if lat is None or lon is None : 
            self.welcome.text = "City not found"
            return
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
        response = requests.get(url).json()
        temp = response["current_weather"]["temperature"]
        humidity = response['hourly']['relativehumidity_2m'][-1]
        weatherype = response["current_weather"]["weathercode"]
        weathercode = {    0: "Clear sky",
                            1: "Mainly clear",
                            2: "Partly cloudy",
                            3: "Overcast",
                            45: "Fog",
                            48: "Depositing rime fog",
                            51: "Light drizzle",
                            53: "Moderate drizzle",
                            55: "Dense drizzle",
                            56: "Light freezing drizzle",
                            57: "Dense freezing drizzle",
                            61: "Slight rain",
                            63: "Moderate rain",
                            65: "Heavy rain",
                            66: "Light freezing rain",
                            67: "Heavy freezing rain",
                            71: "Slight snow fall",
                            73: "Moderate snow fall",
                            75: "Heavy snow fall",
                            77: "Snow grains",
                            80: "Slight rain showers",
                            81: "Moderate rain showers",
                            82: "Violent rain showers",
                            85: "Slight snow showers",
                            86: "Heavy snow showers",
                            95: "Thunderstorm",
                            96: "Thunderstorm with slight hail",
                            99: "Thunderstorm with heavy hail", }
        outsideweather = weathercode.get(weatherype , "Unknown")
        self.Temp.text = f"Current Temperature is : {temp}"
        self.Type.text = f"Outside it is : {outsideweather}"
        self.Humidity.text = f"Current Humidity is : {humidity}"
        self.welcome.text = f"{city}"


        if temp > 30: 
            self.Temp.color = (1, 0, 0, 1)
        elif temp < 25 : 
            self.Temp.color = (0.25, 0.88, 0.82, 1)
        else : self.Temp.color = "#16D325"


        if humidity < 40:
            self.Humidity.color = (0.25, 0.88, 0.82, 1)
        elif humidity <= 70:
            self.Humidity.color ="#16D325"
        else:
            self.Humidity.color = (1, 0, 0, 1)







class WeatherApp(App):
    def build(self):
        return WeatherLayout()
    






if __name__ == "__main__":
    WeatherApp().run()


