# Weather Data API (Flask)

This project is a Flask-based API that fetches historical weather data from an external API and saves it to a MySQL database. The solution includes instructions on setting up the environment, running the server, and testing the API endpoints using **Postman**.

---

## **Project Setup Instructions**

### **1. Prerequisites**

Before setting up and running the API, ensure you have the following installed:
- **Python (3.7+)**
- **MySQL** (For database setup)
- **Git** (For version control)
- **Postman** (For API testing)
- **pip** (Python package installer)

---

### **2. Clone the Repository**
```bash
git clone https://github.com/Praveengoud25/weather_app.git
cd weather-api
```

---

### **3. Set Up Virtual Environment (Recommended)**
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

---

### **4. Install Dependencies**
Install the necessary packages using `pip`:
```bash
pip install -r requirements.txt
```

---

### **5. Set Up MySQL Database**
1. Open MySQL and run the following SQL commands to set up the database and tables:
   ```sql
   CREATE DATABASE quantaco_weather;

   USE quantaco_weather;

   CREATE TABLE Venue (
       id INT PRIMARY KEY AUTO_INCREMENT,
       Name VARCHAR(255),
       Latitude DECIMAL(10, 6),
       Longitude DECIMAL(10, 6)
   );

   -- Inserting sample data into the Venue table
    INSERT INTO Venue (Id, Name, Latitude, Longitude)
    VALUES 
      (1, 'Venue1', 52.52, 13.41),
      (2, 'Venue2', -30.00, 153.125),
      (3, 'Venue3', 44.4375, 26.125);

   CREATE TABLE Weather (
       id INT PRIMARY KEY AUTO_INCREMENT,
       venue_id INT,
       timestamp DATETIME,
       temperature FLOAT,
       humidity FLOAT,
       dewpoint FLOAT,
       apparent_temp FLOAT,
       precipitation FLOAT,
       precipitation_prob FLOAT,
       rain FLOAT,
       showers FLOAT,
       snowfall FLOAT,
       snow_depth FLOAT,
       FOREIGN KEY (venue_id) REFERENCES Venue(id)
   );
   ```
---

### **6. Configure Database Credentials**
1. Open `app.py` and update the database configuration with your MySQL credentials:
   ```python
   db_config = {
       "host": "host_url",
       "user": "db_username",
       "password": "password",
       "database": "quantaco_weather"
   }
   ```

---

### **7. Run the Flask API**
Start the Flask server:
```bash
python weather_data_fetch.py
```
The server should start at **http://127.0.0.1:5000/**.

---

## **API Endpoints**

### **1. Configure Postman for API function**
- **API file:** login into postman app, use import function, Select file option browse to the filename "weather_input.yaml" in the this folder, select the file.

**2. Executing the API**
- **Run** select Run Button on the top right corner of the Screen after API file is imported.

**3. Fetch and Save Weather Data**
- **URL:** `http://127.0.0.1:5000/weather/fetch_and_save`  
- **Method:** `POST`  
- **Description:** Fetches historical weather data for a specific venue and date range, then saves it to the `WeatherData` table.  
- **Sample Request Body:**
  ```json
  {
      "venue_id": 1,
      "start_date": "2023-01-01",
      "end_date": "2023-01-02"
  }
  ```
- **Response Example (Success):**
  ```json
  {
      "status": "success",
      "message": "Weather data saved successfully."
  }
  ```

- **Response Example (Error - Missing Parameter):**
  ```json
  {
      "status": "error",
      "message": "Missing required parameters"
  }
  ```

---

## **Testing the API with Postman**

1. **Open Postman** and create a new request.
2. Set the request type to **POST**.
3. Enter the API URL: `http://127.0.0.1:5000/weather/fetch_and_save`.
4. Go to the **Body** tab and select **raw** > **JSON**.
5. Add the following JSON payload:
   ```json
   {
       "venue_id": 1,
       "start_date": "2023-01-01",
       "end_date": "2023-01-02"
   }
   ```
6. Click **Send** to test the endpoint.
7. Check the response to ensure that data is being saved to the database.

---
By following these instructions, you should be able to set up, run, and test the Flask API locally and interact with it using Postman.