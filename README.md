# Weather-ETL-Project
This project demonstrates a basic ETL pipeline setup that retrieves weather data from the OpenWeather API for Lagos, Nigeria. The data is extracted, transformed, and then loaded into an Amazon S3 bucket. The pipeline is orchestrated using Apache Airflow running on an EC2 instance. IAM roles are used for secure access to the S3 bucket.

![image alt](https://github.com/raphaeloyelami/Weather-ETL-Project/blob/d59b54f808b3be3d20ca0f651255c75b4eb96267/architectural_diagram.png)

- **Source**: OpenWeather API
- **ETL Orchestration**: Apache Airflow
- **Data Storage**: AWS S3
- **Cloud Infrastructure**: AWS EC2 (with IAM role for permissions)
- **Programming Language**: Python
- **IDE**: Visual Studio (via SSH to EC2)

## Prerequisites

1. **AWS EC2 Instance** with an IAM Role that has permissions to access OpenWeather API and S3.
2. **Airflow** installed and running (on EC2).
3. **AWS S3 bucket** to store processed data.
4. **OpenWeather API key** for authentication.
