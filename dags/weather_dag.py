# Import necessary libraries and modules from Airflow
from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor  # Used to check if API is ready
from airflow.operators.python import PythonOperator  # Used for running Python functions
import pandas as pd
import json
from airflow.providers.http.operators.http import HttpOperator  # Used for making HTTP requests

# Function to transform and load the extracted weather data
def transform_load_data(task_instance):
    # Pull the data from XCom (this is the data returned from the extract_weather_data task)
    data = task_instance.xcom_pull(task_ids='extract_weather_data')
    
    # Extract relevant weather details from the data
    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_celsius = data["main"]["temp"]
    feels_like_celsius= data["main"]["feels_like"]
    min_temp_celsius = data["main"]["temp_min"]
    max_temp_celsius = data["main"]["temp_max"]
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    # Create a dictionary with the transformed weather data
    transformed_data = {
        "City": city,
        "Description": weather_description,
        "Temperature (C)": temp_celsius,
        "Feels Like (C)": feels_like_celsius,
        "Minimum Temp (C)":min_temp_celsius,
        "Maximum Temp (C)": max_temp_celsius,
        "Pressure": pressure,
        "Humidity": humidity,
        "Wind Speed": wind_speed,
        "Time of Record": time_of_record,
        "Sunrise (Local Time)":sunrise_time,
        "Sunset (Local Time)": sunset_time
    }

    # Convert the dictionary into a list and then into a DataFrame
    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)

    # AWS credentials for accessing S3 (this is sensitive, you should manage it securely)
    aws_credentials = {
        "key": "",  # Replace with your AWS Access Key ID
        "secret": "",  # Replace with your AWS Secret Access Key
        "token": ""  # Replace with your AWS Session Token
    }

    # Generate a unique filename using the current date and time
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'current_weather_data_lagos_' + dt_string

    # Save the data as a CSV file to an S3 bucket (ensure you have the correct permissions set)
    df_data.to_csv(f"s3://"your_s3_bucket_name"/{dt_string}.csv", index=False, storage_options=aws_credentials)


# Default arguments for the DAG
default_args = {
    'owner': 'ralph',  # The owner of the DAG
    'depends_on_past': False,  # Whether the DAG depends on previous runs
    'start_date': datetime(2023, 1, 8),  # The start date for the DAG
    'email': ['myemail@domain.com'],  # Email notifications for failures
    'email_on_failure': False,  # Disable email on failure
    'email_on_retry': False,  # Disable email on retry
    'retries': 2,  # Number of retries before failing
    'retry_delay': timedelta(minutes=2)  # Delay between retries
}


# Define the DAG
with DAG('weather_dag',
        default_args=default_args,
        schedule_interval = '@daily',  # The DAG will run once a day
        catchup=False) as dag:  # Skip any past DAG runs

    # Define the HttpSensor task to check if the weather API is ready
    is_weather_api_ready = HttpSensor(
        task_id = 'is_weather_api_ready',
        http_conn_id = 'weathermap_api',  # Airflow connection ID for the weather API
        endpoint = '/data/2.5/weather?q=lagos&appid={api_key}&units=metric'
    )

    # Define the HttpOperator task to extract weather data from the API
    extract_weather_data = HttpOperator(
        task_id = 'extract_weather_data',
        http_conn_id = 'weathermap_api',  # Airflow connection ID for the weather API
        endpoint = '/data/2.5/weather?q=lagos&appid={api_key}&units=metric',  # The API endpoint
        method = 'GET',  # HTTP method (GET for retrieving data)
        response_filter = lambda r: json.loads(r.text),  # Filter the response to JSON format
        log_response=True  # Log the response from the API
    )
    
    # Define the PythonOperator task to transform and load the data
    transform_load_weather_data = PythonOperator(
        task_id = 'transform_load_weather_data',  # The task ID
        python_callable = transform_load_data  # The Python function to call
    )


    # Set the task dependencies (task order)
    is_weather_api_ready >> extract_weather_data >> transform_load_weather_data  # Sequential execution order
