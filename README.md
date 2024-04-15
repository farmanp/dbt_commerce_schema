# DBT Commerce Schema

## Project Overview
The `dbt_commerce_schema` leverages a universal schema approach to integrate and transform data from multiple e-commerce platforms (including Brazilian E-commerce and Spotify Storefront) into a unified analytical model. The aim is to provide consistent, reliable analytics across different data sources, enabling cross-platform analysis and reporting.

## Features
- **Universal Schema Design**: Our schema is designed to abstract common dimensions and metrics across different e-commerce platforms, making it easier to perform cross-platform analysis.
- **Data Models**: We include models for orders, payments, and customer interactions that are common across all platforms but may source from different raw data depending on the platform.
- **Scalable Architecture**: The project is built using dbt, allowing for easy deployment, monitoring, and seamless integration with your existing data infrastructure.

## Architecture
The project architecture consists of the following key components:

1. **Data Sources**: Raw data from various e-commerce platforms is ingested into a data lake or data warehouse.
2. **dbt Transformations**: The dbt project reads the raw data, applies transformations, and generates a unified analytical model.
3. **Reporting and Analytics**: The transformed data is used to power dashboards, reports, and other business intelligence tools.

![Project Architecture Diagram](architecture.png)

## Getting Started

### Prerequisites
- Python 3.11
- Poetry (for managing project dependencies).

### Installation
1. Clone this repository to your local machine: `git clone https://github.com/farmanp/dbt-commerce-schema.git`
2. Navigate to the project directory and run `poetry install` to install the project dependencies.
2. Navigate to the `profiles.yml` file and update the connection settings to point to your data warehouse.

### Running the Project
1. Activate the project's virtual environment by running poetry shell.
2. Navigate to the project directory and run:
```
dbt run
dbt test
```
This will execute all models and run tests to validate the transformations.

## Data Models
The project's data models are defined in the `commerce_schema.yml` file. This YAML file describes the entities, their relationships, and the business logic behind the transformations.

![Entity Relationship Diagram](erd.png)

## Deployment and Scheduling
The dbt project is integrated into our CI/CD pipeline, which automatically deploys updates to the production environment. The models are scheduled to run daily using an Airflow DAG, ensuring the analytical data is fresh and up-to-date.

## Monitoring and Alerting
### TODO: 
- Data quality checks on key metrics and dimensions
- Monitoring of model execution times and resource utilization
- Automated alerts for any data anomalies or pipeline failures

## Contributing
To contribute to this project, please create a branch from the `main` branch, make changes, and submit a pull request. Ensure that you add tests for new transformations and update the documentation accordingly.

## Next Steps
- Integrate additional e-commerce platforms (e.g., Shopify, WooCommerce) into the unified analytical model
- Enhance the data models to include more advanced analytical capabilities (e.g., cohort analysis, customer lifetime value)
- Explore opportunities to leverage machine learning and predictive analytics on the transformed data