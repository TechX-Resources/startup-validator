"""
Tests for the web search tool (app/tools/web_search.py).
Run: pytest tests/test_web_search.py -v
"""

from unittest.mock import patch
from app.tools.web_search import web_search, MOCK_RESULTS


class TestWebSearchMockFallback:
    """When SERPAPI_API_KEY is not set, web_search returns mock data."""

    @patch.dict("os.environ", {}, clear=True)
    def test_returns_mock_when_no_api_key(self):
        results = web_search("test query")
        assert results == MOCK_RESULTS

    @patch.dict("os.environ", {}, clear=True)
    def test_respects_max_results_with_mock(self):
        results = web_search("test query", max_results=1)
        assert len(results) == 1

    @patch.dict("os.environ", {}, clear=True)
    def test_mock_results_have_expected_keys(self):
        results = web_search("test query")
        for r in results:
            assert "title" in r
            assert "snippet" in r
            assert "link" in r


class TestWebSearchResultFormat:
    """Verify the shape of results regardless of source."""

    @patch.dict("os.environ", {}, clear=True)
    def test_returns_list(self):
        results = web_search("test query")
        assert isinstance(results, list)

    @patch.dict("os.environ", {}, clear=True)
    def test_each_result_is_dict(self):
        results = web_search("test query")
        for r in results:
            assert isinstance(r, dict)


class TestWebSearchAPIError:
    """When SerpAPI fails, web_search falls back to mock data."""

    @patch("app.tools.web_search.httpx.get", side_effect=Exception("API down"))
    @patch.dict("os.environ", {"SERPAPI_API_KEY": "fake-key"})
    def test_falls_back_to_mock_on_api_error(self, mock_get):
        results = web_search("test query")
        assert results == MOCK_RESULTS[:5]

    @patch("app.tools.web_search.httpx.get")
    @patch.dict("os.environ", {"SERPAPI_API_KEY": "fake-key"})
    def test_parses_organic_results(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.raise_for_status = lambda: None
        mock_get.return_value.json.return_value = {
            "organic_results": [
                {"title": "Result 1", "snippet": "Snippet 1", "link": "https://example.com/1"},
                {"title": "Result 2", "snippet": "Snippet 2", "link": "https://example.com/2"},
            ]
        }
        results = web_search("test query", max_results=2)
        assert len(results) == 2
        assert results[0]["title"] == "Result 1"
        assert results[1]["link"] == "https://example.com/2"
