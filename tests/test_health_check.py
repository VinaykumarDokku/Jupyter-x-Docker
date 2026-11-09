import unittest
from unittest.mock import patch, MagicMock

from scripts.health_check import check_jupyter_health


class TestHealthCheck(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_healthy_server(self, mock_urlopen):
        response = MagicMock()
        response.status = 200
        mock_urlopen.return_value.__enter__.return_value = response

        self.assertTrue(check_jupyter_health())

    @patch("urllib.request.urlopen")
    def test_unhealthy_server(self, mock_urlopen):
        response = MagicMock()
        response.status = 503
        mock_urlopen.return_value.__enter__.return_value = response

        self.assertFalse(check_jupyter_health())

    @patch("urllib.request.urlopen")
    def test_connection_failure(self, mock_urlopen):
        from urllib.error import URLError

        mock_urlopen.side_effect = URLError("Connection refused")

        self.assertFalse(check_jupyter_health())


if __name__ == "__main__":
    unittest.main()
