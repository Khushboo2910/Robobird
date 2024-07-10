import requests

API_KEY = 'e58e5c6591778d8d7079d0867bdc54c0'  
BASE_URL = 'http://api.openweathermap.org/data/2.5/'

def get_weather_data(city):
    try:
        current_weather_url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
      
        response = requests.get(current_weather_url)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"Current Weather in {data['name']}:")
            print(f"Temperature: {data['main']['temp']}°C")
            print(f"Weather: {data['weather'][0]['description']}")
            print(f"Humidity: {data['main']['humidity']}%")
            print(f"Wind Speed: {data['wind']['speed']} m/s")
        else:
            data = response.json()
            print(f"Error: {data['message']}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    city = input("Enter the city name: ")
    get_weather_data(city)

if __name__ == '__main__':
    main()
