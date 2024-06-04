import json
from typing import Dict

from google.cloud.bigquery.client import Client
from google.oauth2 import service_account

_BQ_DEFAULT_LOCATION = "US"
_GCP_PRIVATE_KEY_PREFIX = "-----BEGIN PRIVATE KEY-----"
_GCP_PRIVATE_KEY_SUFFIX = "-----END PRIVATE KEY-----"


def _get_service_account_info(service_account_json: str, private_key: str) -> Dict:
    service_account_info: Dict = json.loads(service_account_json)
    gcp_private_key = "\n".join(
        [_GCP_PRIVATE_KEY_PREFIX, private_key, _GCP_PRIVATE_KEY_SUFFIX]
    )
    service_account_info["private_key"] = gcp_private_key
    return service_account_info


def get_client(
    project: str,
    service_account_json: str,
    private_key: str,
    location: str = _BQ_DEFAULT_LOCATION,
) -> Client:
    service_account_info: Dict = _get_service_account_info(
        service_account_json, private_key
    )
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info
    )
    client = Client(project=project, credentials=credentials, location=location)
    return client
