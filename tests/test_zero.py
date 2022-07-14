from unittest import mock
import aiohttp

import pytest
from zero_sdk import zero

API_RESPONSE_MOCK = {"data": {"secrets": [{"name": "test", "fields": [{"name": "name", "value": "value"}]}]}}


class QueryMock(mock.MagicMock):
    async def __call__(self, *_, **kwargs):
        if len(kwargs["variables"]["apis"]) == 0:
            raise aiohttp.client_exceptions.ServerDisconnectedError

        if kwargs["variables"]["token"] == "token":
            return API_RESPONSE_MOCK

        return {"data": {"secrets": []}}


class TestZero:
    def test_non_empty_token_provided(self):
        pytest.raises(AssertionError, zero, token="", apis=["aws"])

    @mock.patch("python_graphql_client.GraphqlClient.execute_async", new_callable=QueryMock)
    def test_response_body_structure(self, _):
        assert zero(
            token="token",
            pick=["aws"]
        ).fetch() == {"test": {"name": "value"}}, "Response body is not as expected"

    @mock.patch("python_graphql_client.GraphqlClient.execute_async", new_callable=QueryMock)
    def test_empty_response_body_structure(self, _):
        assert zero(
            token="invalid token",
            pick=["aws"]
        ).fetch() == {}, "Response body is not as expected"

    @mock.patch("python_graphql_client.GraphqlClient.execute_async", new_callable=QueryMock)
    def test_raise_exception_if_fetch_failed(self, _):
        with pytest.raises(aiohttp.client_exceptions.ServerDisconnectedError):
            zero(token="token", pick=[]).fetch()
