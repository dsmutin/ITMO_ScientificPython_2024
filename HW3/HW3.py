import openmeteo_requests

class IncreaseSpeed():
    '''
    Iterator for increasing the speed with the default step of 10 km/h
    You can implement this one after Iterators FP topic

    Constructor params: 
      current_speed: a value to start with, km/h
      max_speed: a maximum possible value, km/h

    Make sure your iterator is not exceeding the maximum allowed value
    '''

    def __init__(self, current_speed: int, max_speed: int, step: int=10):
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        self.current_speed += self.step
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed
            raise StopIteration
        return self.current_speed


class DecreaseSpeed():
    '''
    Iterator for decreasing the speed with the default step of 10 km/h
    You can implement this one after Iterators FP topic 

    Constructor params: 
      current_speed: a value to start with, km/h

    Make sure your iterator is not going below zero
    '''

    def __init__(self, current_speed: int, min_speed: int, step: int=10):
        self.current_speed = current_speed
        self.min_speed = min_speed
        self.step = step
        if min_speed < 0:
            return ValueError("Minimal speed below 0")

    def __iter__(self):
        return self

    def __next__(self):
        self.current_speed -= self.step
        if self.current_speed < self.min_speed:
            self.current_speed = self.min_speed
            raise StopIteration
        return self.current_speed


class Car():
    '''
    Car class. 
    Has a class variable for counting total amount of cars on the road (increased by 1 upon instance initialization).

    Constructor params:
      max_speed: a maximum possible speed, km/h
      current_speed: current speed, km/h (0 by default)
      state: reflects if the Car is in the parking or on the road

    Methods:
      accelerate: increases the speed using IncreaseSpeed() iterator either once or gradually to the upper_border
      brake: decreases the speed using DecreaseSpeed() iterator either once or gradually to the lower_border
      parking: if the Car is not already in the parking, removes the Car from the road
      total_cars: show the total amount of cars on the road
      show_weather: shows the current weather conditions
    '''
    car_number = 0

    def __init__(self, max_speed: int, current_speed: int=0, state: bool=True):
        self.max_speed = max_speed
        self.current_speed = current_speed
        self.state = state
        Car.car_number += 1
        pass

    def accelerate(self, upper_border=None):
        if self.state:
            if upper_border is None:
                self.current_speed += 10
                if self.current_speed > self.max_speed:
                    self.current_speed = self.max_speed
                print(f'Speed increased to: {self.current_speed}')
            else:
                if upper_border > self.max_speed:
                    return ValueError("Upper border is bigger than max speed")
                if upper_border < self.current_speed:
                    return ValueError("Upper border is less than current spped")
                else:
                    Increase_Speed = IncreaseSpeed(current_speed=self.current_speed, max_speed=upper_border)
                    for speed in Increase_Speed:
                        self.current_speed = speed
                        print(f'Speed increased to: {speed}')
            print(f'Current speed is: {self.current_speed}')

        else:
            return ValueError("Already parked")
        # check for state
        # create an instance of IncreaseSpeed iterator
        # check if smth passed to upper_border and if it is valid speed value
        # if True, increase the speed gradually iterating over your increaser until upper_border is met
        # print a message at each speed increase
        # else increase the speed once
        # return the message with current speed
        pass

    def brake(self, lower_border=None):
        if self.state:
            if lower_border is None:
                self.current_speed -= 10
                if self.current_speed < 0:
                    self.current_speed = 0
            else:
                if lower_border < 0:
                    return ValueError("Lower border is below zero")
                if lower_border > self.current_speed:
                    return ValueError("Lower border is bigger than current spped")
                else:
                    Decrease_Speed = DecreaseSpeed(current_speed=self.current_speed, min_speed=lower_border)
                    for speed in Decrease_Speed:
                        self.current_speed = speed
                        print(f'Speed decreased to: {speed}')
            print(f'Current speed is: {self.current_speed}')

        else:
            return ValueError("Already parked")
        # create an instance of DecreaseSpeed iterator
        # check if smth passed to lower_border and if it is valid speed value
        # if True, decrease the speed gradually iterating over your decreaser until lower_border is met
        # print a message at each speed decrease
        # else increase the speed once
        # return the message with current speed
        pass

    # the next three functions you have to define yourself
    # one of the is class method, one - static and one - regular method (not necessarily in this order, it's for you to think)

    def parking(self):
        if self.state:
            self.state=False
            Car.car_number -= 1
        else:
            return ValueError("Already parked")
        # gets car off the road (use state and class variable)
        # check: should not be able to move the car off the road if it's not there

    @classmethod
    def total_cars(cls):
        print(f'Number of cars on the road: {cls.car_number}')
        # displays total amount of cars on the road

    @staticmethod
    def show_weather():
        openmeteo = openmeteo_requests.Client()
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
        "latitude": 59.9386, # for St.Petersburg
        "longitude": 30.3141, # for St.Petersburg
        "current": ["temperature_2m", "apparent_temperature", "rain", "wind_speed_10m"],
        "wind_speed_unit": "ms",
        "timezone": "Europe/Moscow"
        }

        response = openmeteo.weather_api(url, params=params)[0]

        # The order of variables needs to be the same as requested in params->current!
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_rain = current.Variables(2).Value()
        current_wind_speed_10m = current.Variables(3).Value()

        print(f'\nThere is no sunshine in St. Petersburg, but current weather is:')
        print(f"temperature: {round(current_temperature_2m, 1)} °C")
        print(f"apparent temperature: {round(current_apparent_temperature, 1)} °C")
        print(f"rain: {current_rain} mm")
        print(f"wind speed: {round(current_wind_speed_10m, 1)} m/s")
