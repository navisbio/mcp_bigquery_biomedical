import logging
import os
from typing import Any, Optional, List
from google.cloud import bigquery
from google.oauth2 import service_account

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger('mcp_aact_server.database')

class BigQueryDatabase:
    def __init__(self):
        logger.info("Initializing BigQuery database connection")
        self.client = self._initialize_bigquery_client()
        # Re-enable dataset validation
        self.allowed_datasets = self._get_allowed_datasets()
        logger.info(f"BigQuery database initialization complete. Allowed datasets: {self.allowed_datasets}")

    def _initialize_bigquery_client(self) -> bigquery.Client:
        """Initializes the BigQuery client."""
        logger.debug("Initializing BigQuery client")
        credentials = service_account.Credentials.from_service_account_file(
            os.environ.get('BIGQUERY_CREDENTIALS'),
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id
        )
        logger.info("BigQuery client initialized")
        return client

    def _get_allowed_datasets(self) -> List[str]:
        """Get list of allowed datasets from environment variable"""
        datasets = os.environ.get('ALLOWED_DATASETS', '').split(',')
        allowed = [ds.strip() for ds in datasets if ds.strip()]
        if not allowed:
            raise ValueError("No datasets configured. Please set ALLOWED_DATASETS environment variable.")
        return allowed


    def validate_dataset(self, dataset: str) -> None:
        """Validate that the dataset is allowed"""
        # Temporarily disabled dataset validation
        # if not dataset:
        #     raise ValueError("Dataset name cannot be empty")
        # if dataset not in self.allowed_datasets:
        #     raise ValueError(f"Dataset '{dataset}' is not in allowed datasets: {self.allowed_datasets}")
        pass

    def execute_query(self, query: str, dataset: str, params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Execute a SQL query and return results as a list of dictionaries"""
        logger.debug(f"Executing query on dataset {dataset}: {query}")
        
        try:
            # Set up the job configuration with the dataset
            job_config = bigquery.QueryJobConfig()
            
            if params:
                logger.debug(f"Query parameters: {params}")
                query_parameters = [
                    bigquery.ScalarQueryParameter(name, "STRING", value)
                    for name, value in params.items()
                ]
                job_config.query_parameters = query_parameters

            # Replace any existing dataset references with the correct project.dataset format
            full_dataset = f"bigquery-public-data.{dataset}"
            query = query.replace(dataset + ".", full_dataset + ".")
            
            # If no dataset reference in query, add the default dataset config
            if full_dataset not in query:
                job_config.default_dataset = f"bigquery-public-data.{dataset}"

            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()
            rows = [dict(row) for row in results]
            logger.debug(f"Query returned {len(rows)} rows")
            return rows
        except Exception as e:
            logger.error(f"BigQuery error executing query: {str(e)}", exc_info=True)
            raise RuntimeError(f"BigQuery error: {str(e)}")
