import requests
from math import radians, cos, sin, sqrt, atan2
from typing import List, Any, Dict

class Vehicle:
    """Class representing a vehicle with basic attributes."""
    
    def __init__(self, id: Any = None, name: str = None, model: str = None, year: int = None, color: str = None, price: float = None, latitude: float = None, longitude: float = None):
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"

class VehicleManager:
    """Class for managing Vehicle data with REST API adjustments."""
    
    def __init__(self, url: str):
        self.url = url

    def get_vehicles(self) -> List[Vehicle]:
        """Fetches a list of vehicles from the API."""
        response = requests.get(f"{self.url}/vehicles")
        vehicles = [Vehicle(**vehicle) for vehicle in response.json()]
        return vehicles

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        """Fetches a specific vehicle by vehicle ID."""
        response = requests.get(f"{self.url}/vehicles/{vehicle_id}")
        vehicle_data = response.json()
        return Vehicle(**vehicle_data)

    def add_vehicle(self, vehicle: Vehicle) -> Any:
        """Adds a new vehicle to the API, requiring a manual 'id' since the test server does not auto-generate it."""
        response = requests.post(f"{self.url}/vehicles", json=vars(vehicle))
        if response.status_code == 200:
            return Vehicle(**response.json())
        elif 'id' in response.json() and 'This field may not be null.' in response.json()['id']:
            print("Ошибка: Поле 'id' не может быть пустым. id не генерится на тестовом сервере, поэтому нужно указать id в запросе")
        else:
            return f"Failed to add vehicle: {response.text}"

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        """Updates a vehicle's information by ID."""
        response = requests.put(f"{self.url}/vehicles/{vehicle.id}", json=vars(vehicle))
        return Vehicle(**response.json())

    def delete_vehicle(self, id: int) -> int:
        """Deletes a vehicle by its ID."""
        response = requests.delete(f"{self.url}/vehicles/{id}")
        return response.status_code

    def filter_vehicles(self, params: Dict[str, Any]) -> List[Vehicle]:
        """Filters vehicles based on specified key-value parameters."""
        all_vehicles = self.get_vehicles()
        filtered_vehicles = [
            vehicle for vehicle in all_vehicles 
            if all(getattr(vehicle, key) == value for key, value in params.items())
        ]
        return filtered_vehicles

    def get_distance(self, id1: int, id2: int) -> float:
        """Calculates the distance in meters between two vehicles using their coordinates."""
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)
        lat1, lon1 = radians(vehicle1.latitude), radians(vehicle1.longitude)
        lat2, lon2 = radians(vehicle2.latitude), radians(vehicle2.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6371000 * c  # Earth's radius in meters
        return distance

    def get_nearest_vehicle(self, id: int) -> Vehicle:
        """Finds the nearest vehicle to a given vehicle identified by ID."""
        target_vehicle = self.get_vehicle(id)
        all_vehicles = self.get_vehicles()
        min_distance = float('inf')
        nearest_vehicle = None
        for vehicle in all_vehicles:
            if vehicle.id != id:
                distance = self.get_distance(id, vehicle.id)
                if distance < min_distance:
                    min_distance = distance
                    nearest_vehicle = vehicle
        print("Ответ возможно будет неверным!")
        return nearest_vehicle
