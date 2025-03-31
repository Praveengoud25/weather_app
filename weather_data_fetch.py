from flask import Flask, request, jsonify
import requests
import mysql.connector
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Database connection setup (update these with your DB details)
db_config = {
    "host": "localhost",
    "user": "sqluser",
    "password": "Prav@1133",
    "database": "quantaco_weather"
}


# Open-Meteo API endpoint
WEATHER_API_URL = "https://archive-api.open-meteo.com/v1/archive"

# API Route to fetch and save weather data
@app.route('/weather/fetch_and_save', methods=['POST'])
def fetch_and_save_weather():
    data = request.json

    # Extract venue_id, start_date, and end_date from the request
    venue_id = data.get("venue_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    # Validate input
    if not venue_id or not start_date or not end_date:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400

    #dateformeat check
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format. Use YYYY-MM-DD."}), 400
        
    conn = None
    cursor = None
    try:
        # Connect to the database and get venue details
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Venue WHERE id = %s", (venue_id,))
        venue = cursor.fetchone()

        if not venue:
            return jsonify({"status": "error", "message": f"Venue with id {venue_id} not found"}), 404

        # Get latitude and longitude from the venue table
        latitude = venue['Latitude']
        longitude = venue['Longitude']

        # Fetch weather data from the external API
        response = requests.get(
            WEATHER_API_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "hourly": "temperature_2m,relative_humidity_2m,dewpoint_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth"
            }
        )

        if response.status_code != 200:
            return jsonify({"status": "error", "message": "Failed to fetch weather data from external API"}), 500
        
        #data_formating check

        weather_data = response.json()
        if "hourly" not in weather_data:
            return jsonify({"status": "error", "message": "Failed to fetch weather data"}), 500

        # Save weather data to the database
        for i in range(len(weather_data["hourly"]["time"])):
            timestamp = weather_data["hourly"]["time"][i]
            temperature = weather_data["hourly"]["temperature_2m"][i]
            humidity = weather_data["hourly"]["relative_humidity_2m"][i]
            dewpoint = weather_data["hourly"]["dewpoint_2m"][i]
            apparent_temp = weather_data["hourly"]["apparent_temperature"][i]
            precipitation = weather_data["hourly"]["precipitation"][i]
            precipitation_prob = weather_data["hourly"]["precipitation_probability"][i]
            rain = weather_data["hourly"]["rain"][i]
            showers = weather_data["hourly"]["showers"][i]
            snowfall = weather_data["hourly"]["snowfall"][i]
            snow_depth = weather_data["hourly"]["snow_depth"][i]
#pull dta into cache table.
    #check the attributes temp 100 => write error table or else weather table
    #
    #write data fro cache to table.

            # Insert into weather table
            cursor.execute(
                """
                INSERT INTO weather (venue_id, timestamp, temperature, humidity, dewpoint, apparent_temp, precipitation, precipitation_prob, rain, showers, snowfall, snow_depth)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (venue_id, timestamp, temperature, humidity, dewpoint, apparent_temp, precipitation, precipitation_prob, rain, showers, snowfall, snow_depth)
            )

        conn.commit()

        return jsonify({"status": "success", "message": "Weather data saved successfully."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)