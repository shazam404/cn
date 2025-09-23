import socket
import json

def format_weather_report(weather_data):
    if weather_data.get("status") == "error":
        return f"Error: {weather_data.get('message', 'Unknown error')}"
    
    if weather_data.get("status") == "disconnect":
        return f"👋 {weather_data.get('message', 'Goodbye!')}"
    
    city = weather_data.get("city", "Unknown")
    temp = weather_data.get("temperature", "N/A")
    humidity = weather_data.get("humidity", "N/A")
    conditions = weather_data.get("conditions", "N/A")
    wind_speed = weather_data.get("wind_speed", "N/A")
    pressure = weather_data.get("pressure", "N/A")
    note = weather_data.get("note", "")
    
    report = f"""
╔══════════════════════════════════════════════════════════╗
║                    🌤️  WEATHER REPORT                    ║
╠══════════════════════════════════════════════════════════╣
║  City:        {city:<40} ║
║  Temperature: {temp:<40} ║
║  Humidity:    {humidity:<40} ║
║  Conditions:  {conditions:<40} ║
║  Wind Speed:  {wind_speed:<40} ║
║  Pressure:    {pressure:<40} ║"""
    
    if note:
        report += f"""
║                                                          ║
║  Note: {note:<46} ║"""
    
    report += """
╚══════════════════════════════════════════════════════════╝
"""
    return report

def run_weather_client(host="127.0.0.1", port=9090):
    """Run the weather query client"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to weather server
        client.connect((host, port))
        print(f"🌐 Connected to Weather Service at {host}:{port}")
        print("=" * 60)
        print("Welcome to Weather Query Service!")
        print("Enter a city name to get weather information")
        print("Try cities like: Mumbai, Delhi, Bangalore, New York")
        print("Type 'quit', 'exit', or 'bye' to disconnect")
        print("=" * 60)
        
        while True:
            city_name = input("\nEnter city name: ").strip()
            
            if not city_name:
                print("Please enter a valid city name")
                continue
            
            client.send(city_name.encode('utf-8'))
            
            response = client.recv(2048).decode('utf-8')
            
            try:
                weather_data = json.loads(response)
                
                if weather_data.get("status") == "disconnect":
                    print(format_weather_report(weather_data))
                    break
                
                formatted_report = format_weather_report(weather_data)
                print(formatted_report)
                
            except json.JSONDecodeError:
                print("Error: Invalid response from server")
            
    except ConnectionRefusedError:
        print("Could not connect to weather server.")
    except Exception as e:
        print(f"Client error: {e}")
    
    finally:
        client.close()
        print("\nDisconnected from Weather Service. Goodbye!")

if __name__ == "__main__":
    run_weather_client()

#python3 client.py
