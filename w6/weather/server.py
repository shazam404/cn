import socket
import threading
import json
import random

# Simulated weather database
WEATHER_DATA = {
    "mumbai": {
        "temperature": "28°C",
        "humidity": "75%",
        "conditions": "Partly Cloudy",
        "wind_speed": "15 km/h",
        "pressure": "1013 hPa"
    },
    "delhi": {
        "temperature": "32°C",
        "humidity": "45%",
        "conditions": "Clear Sky",
        "wind_speed": "12 km/h",
        "pressure": "1015 hPa"
    },
    "bangalore": {
        "temperature": "24°C",
        "humidity": "60%",
        "conditions": "Light Rain",
        "wind_speed": "8 km/h",
        "pressure": "1012 hPa"
    },
    "new york": {
        "temperature": "18°C",
        "humidity": "50%",
        "conditions": "Cool Breeze",
        "wind_speed": "20 km/h",
        "pressure": "1018 hPa"
    }
}

def get_weather_data(city_name):
    city_lower = city_name.lower().strip()
    
    if city_lower in WEATHER_DATA:
        weather = WEATHER_DATA[city_lower].copy()
        weather["city"] = city_name.title()
        weather["status"] = "success"
        return weather
    else:
        # Generate random weather data for unknown cities
        temp = random.randint(15, 35)
        humidity = random.randint(30, 90)
        conditions_list = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Overcast", "Clear"]
        
        return {
            "city": city_name.title(),
            "temperature": f"{temp}°C",
            "humidity": f"{humidity}%",
            "conditions": random.choice(conditions_list),
            "wind_speed": f"{random.randint(5, 25)} km/h",
            "pressure": f"{random.randint(1005, 1025)} hPa",
            "status": "success",
            "note": "Weather data generated (city not in database)"
        }

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected to weather service.")
    
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            
            if not data:
                break
            
            city_name = data.strip()
            print(f"[{addr}] Weather query for: {city_name}")
            
            if city_name.lower() in ['quit', 'exit', 'bye']:
                response = {
                    "status": "disconnect",
                    "message": "Thank you for using Weather Service!"
                }
                conn.send(json.dumps(response).encode('utf-8'))
                break
            
            weather_data = get_weather_data(city_name)
            
            response = json.dumps(weather_data, indent=2)
            conn.send(response.encode('utf-8'))
            
    except Exception as e:
        print(f"[ERROR] Error handling client {addr}: {e}")
        error_response = {
            "status": "error",
            "message": f"Server error: {str(e)}"
        }
        try:
            conn.send(json.dumps(error_response).encode('utf-8'))
        except:
            pass
    
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected from weather service.")

def start_weather_server(host="127.0.0.1", port=9090):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reuse of address
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[LISTENING] Weather Service running on {host}:{port}")
        print(f"[INFO] Available cities: {', '.join(WEATHER_DATA.keys())}")
        print(f"[INFO] Server can also generate weather for unknown cities")
        print(f"[INFO] Waiting for weather queries...")
        
        while True:
            conn, addr = server.accept()
            
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
            
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    
    finally:
        server.close()

if __name__ == "__main__":
    start_weather_server()

#python3 server.py
