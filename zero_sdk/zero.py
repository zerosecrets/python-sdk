"""Zero SDK for Python"""
import asyncio
from typing import List, Dict, Optional

from python_graphql_client import GraphqlClient


class ZeroException(Exception):
    pass


class ZeroApiClient:
    """The Zero API"""

    query = """
        query Secrets($token: String!, $pick: [String!], callerName: String) {
            secrets(zeroToken: $token, pick: $pick, callerName: $callerName) {
                name

                fields {
                    name
                    value
                }
            }
        }
    """

    def __init__(self, url: str, token: str, pick: List[str], caller_name: Optional[str]):
        self.client = GraphqlClient(endpoint=url)
        self.variables = {"token": token, "pick": pick, "callerName": caller_name}

    def fetch(self) -> Dict[str, Dict[str, str]]:
        """Grab the secrets from the Zero API"""

        response_body = asyncio.run(
            self.client.execute_async(
                query=self.query,
                variables=self.variables
            )
        )

        if response_body.get('errors') is not None:
            raise ZeroException(response_body.get('errors')[0].get('message'))

        try:
            return {
                secret.get("name"): {
                    field.get("name"): field.get("value") for field in secret.get("fields")
                } for secret in response_body.get("data").get("secrets")
            }
        except AttributeError:
            raise AttributeError('Pick should be a list of strings')


def zero(*, token: str, pick: List[str], caller_name: Optional[str]) -> ZeroApiClient:
    """Create a Zero API client"""

    assert type(token) is str, "Zero token should be str"
    assert len(token) > 0, "Zero token is required"
    assert type(pick) is list, "Pick should be a list of strings"

    return ZeroApiClient("https://core.tryzero.com/v1/graphql", token, pick, caller_name)
