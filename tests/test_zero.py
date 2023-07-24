from unittest import mock

import pytest
from zero_python_sdk import zero, ZeroException

API_RESPONSE_MOCK = {"data": {"secrets": [{"name": "test", "fields": [{"name": "name", "value": "value"}]}]}}


class QueryMock(mock.MagicMock):
    async def __call__(self, *_, **kwargs):
        if len(kwargs["variables"]["pick"]) == 0:
            return {
                "data": None,

                "errors": [
                    {
                        "message": 'Could not establish connection with database',
                        "locations": [{"line": 2, "column": 2}],
                        "path": ['secrets'],
                        "extensions": {
                            "internal_error":
                                'Error occurred while creating a new object: error connecting to server:' +
                                'Connection refused (os error 61)',
                        },
                    }
                ]
            }

        if kwargs["variables"]["token"] == "token":
            return API_RESPONSE_MOCK

        return {"data": {"secrets": []}}


class TestZero:
    def test_non_empty_token_provided(self):
        pytest.raises(AssertionError, zero, token="", pick=["aws"], caller_name=None)

    @mock.patch("python_graphql_client.GraphqlClient.execute_async", new_callable=QueryMock)
    def test_response_body_structure(self, _):
        assert zero(
            token="token",
            pick=["aws"],
            caller_name=None,
        ).fetch() == {"test": {"name": "value"}}, "Response body is not as expected"

    @mock.patch("python_graphql_client.GraphqlClient.execute_async", new_callable=QueryMock)
    def test_empty_response_body_structure(self, _):
        assert zero(
            token="invalid token",
            pick=["aws"],
            caller_name=None,
        ).fetch() == {}, "Response body is not as expected"

    @mock.patch("python_graphql_client.GraphqlClient.execute_async", new_callable=QueryMock)
    def test_raise_exception_if_fetch_failed(self, _):
        with pytest.raises(ZeroException):
            zero(token="token", pick=[], caller_name=None).fetch()
