import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import json


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    yield Path(temp_file.name)
    Path(temp_file.name).unlink(missing_ok=True)


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ],
        "products": [
            {"id": 1, "name": "Widget A", "price": 19.99},
            {"id": 2, "name": "Widget B", "price": 29.99}
        ]
    }


@pytest.fixture
def mock_config():
    """Provide a mock configuration object."""
    config = Mock()
    config.DEBUG = True
    config.TESTING = True
    config.SECRET_KEY = "test-secret-key"
    config.DATABASE_URL = "sqlite:///:memory:"
    return config


@pytest.fixture
def mock_database():
    """Provide a mock database connection."""
    db = MagicMock()
    db.execute.return_value = Mock()
    db.fetchone.return_value = None
    db.fetchall.return_value = []
    db.commit.return_value = None
    return db


@pytest.fixture
def mock_logger():
    """Provide a mock logger."""
    logger = Mock()
    logger.debug = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    logger.critical = Mock()
    return logger


@pytest.fixture
def mock_requests():
    """Provide a mock requests object for HTTP testing."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_response.text = '{"status": "success"}'
    mock_response.headers = {"Content-Type": "application/json"}
    
    mock_session = Mock()
    mock_session.get.return_value = mock_response
    mock_session.post.return_value = mock_response
    mock_session.put.return_value = mock_response
    mock_session.delete.return_value = mock_response
    
    return mock_session


@pytest.fixture
def json_file(temp_dir):
    """Create a temporary JSON file with sample data."""
    data = {"test": True, "value": 42, "items": ["a", "b", "c"]}
    json_path = temp_dir / "test_data.json"
    with open(json_path, "w") as f:
        json.dump(data, f)
    return json_path


@pytest.fixture
def text_file(temp_dir):
    """Create a temporary text file with sample content."""
    content = "This is a test file.\nIt has multiple lines.\nFor testing purposes."
    text_path = temp_dir / "test_file.txt"
    with open(text_path, "w") as f:
        f.write(content)
    return text_path


@pytest.fixture(scope="session")
def test_session_data():
    """Provide session-scoped test data."""
    return {
        "session_id": "test-session-12345",
        "created_at": "2023-01-01T00:00:00Z",
        "test_mode": True
    }


@pytest.fixture
def mock_environment(monkeypatch):
    """Set up a mock environment with test variables."""
    test_env = {
        "FLASK_ENV": "testing",
        "DATABASE_URL": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key-12345",
        "DEBUG": "True"
    }
    
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    
    return test_env


@pytest.fixture
def capture_logs(caplog):
    """Helper fixture to capture and provide easy access to logs."""
    caplog.set_level("DEBUG")
    return caplog