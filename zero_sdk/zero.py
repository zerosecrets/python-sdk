"""Zero SDK for Python"""
import asyncio
from typing import List, Dict

from python_graphql_client import GraphqlClient


class ZeroApiClient:
    """The Zero API"""

    query = """
        query Secrets($token: String!, $apis: [String!]) {
            secrets(zeroToken: $token, pick: $apis) {
                name

                fields {
                    name
                    value
                }
            }
        }
    """

    def __init__(self, url: str, token: str, apis: List[str]):
        self.client = GraphqlClient(endpoint=url)
        self.variables = {"token": token, "apis": apis}

    def fetch(self) -> Dict[str, Dict[str, str]]:
        """Grab the secrets from the Zero API"""

        response_body = asyncio.run(
            self.client.execute_async(
                query=self.query,
                variables=self.variables
            )
        )

        try:
            return {
                secret.get("name"): {
                    field.get("name"): field.get("value") for field in secret.get("fields")
                } for secret in response_body.get("data").get("secrets")
            }
        except AttributeError:
            raise AttributeError('Apis should be a list of strings')


def zero(*, token: str, apis: List[str]) -> ZeroApiClient:
    """Create a Zero API client"""

    assert type(token) is str, "Zero token should be str"
    assert len(token) > 0, "Zero token is required"
    assert type(apis) is list, "Apis should be a list of strings"

    return ZeroApiClient("https://core.tryzero.com/v1/graphql", token, apis)
