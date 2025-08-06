import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from mock_environment import mock_openai_environment, mock_azure_openai_environment


def test_mock_openai_environment():
    original = os.environ.get("OPENAI_API_KEY")
    with mock_openai_environment():
        assert os.environ["OPENAI_API_KEY"] == "sk-test"
    assert os.environ.get("OPENAI_API_KEY") == original


def test_mock_azure_openai_environment():
    original = os.environ.get("AZURE_OPENAI_API_KEY")
    with mock_azure_openai_environment():
        assert os.environ["AZURE_OPENAI_API_KEY"] == "test-key"
    assert os.environ.get("AZURE_OPENAI_API_KEY") == original
