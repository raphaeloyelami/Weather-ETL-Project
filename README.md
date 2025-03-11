# Weather-ETL-Project
This project demonstrates a basic ETL pipeline setup that retrieves weather data from the OpenWeather API for Lagos, Nigeria. The data is extracted, transformed, and then loaded into an Amazon S3 bucket. The pipeline is orchestrated using Apache Airflow running on an EC2 instance. IAM roles are used for secure access to the S3 bucket.

![image alt](https://github.com/raphaeloyelami/Weather-ETL-Project/blob/bf80f753396d53424463e93d338e8c2f0db97b18/architecture/architectural_diagram.png)

# Project Overview

## Extract
Data is pulled from the [OpenWeather API](https://openweathermap.org/api)

## Transform
Data is cleaned and transformed (for example, converting units, filtering, etc.).

## Load
The transformed data is stored in an S3 bucket for further analysis.

The ETL process is orchestrated using **Apache Airflow**, which is deployed on an AWS EC2 instance. The project leverages **IAM roles** for security, and **SSH** is used to interact with the EC2 instance.

---

# Project Components

1. **OpenWeather API**  
   - Extract weather data.

2. **AWS EC2**  
   - Hosts Apache Airflow for orchestrating the ETL process.

3. **Apache Airflow**  
   - Used to schedule and manage the workflow.

4. **S3**  
   - The transformed data is stored in an S3 bucket.

5. **IAM Roles**  
   - To manage access between AWS services.

6. **SSH**  
   - Used to connect to the EC2 instance.

---

# Prerequisites

Before setting up the project, ensure you have:

- AWS Account with appropriate permissions.
- IAM Role for EC2 with access to S3 and necessary services.
- Airflow installed on EC2 (if not using AWS-managed Airflow).
- OpenWeather API Key.


