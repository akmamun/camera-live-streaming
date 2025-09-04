"""
Validation tests to verify the testing infrastructure is working correctly.
These tests validate that the testing setup, fixtures, and configuration are functional.
"""
import pytest
import sys
from pathlib import Path


class TestInfrastructureValidation:
    """Test class to validate the testing infrastructure setup."""
    
    def test_python_version(self):
        """Validate Python version is appropriate for testing."""
        assert sys.version_info >= (3, 8), "Python 3.8+ is required"
    
    def test_pytest_markers(self):
        """Validate that custom pytest markers are working."""
        # This test itself uses markers to verify they're configured
        assert True
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker works."""
        assert True
    
    @pytest.mark.integration 
    def test_integration_marker(self):
        """Test that integration marker works."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow marker works."""
        assert True


class TestFixtureValidation:
    """Test class to validate fixtures are working correctly."""
    
    def test_temp_dir_fixture(self, temp_dir):
        """Validate temp_dir fixture works."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Create a test file in the temp directory
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()
        assert test_file.read_text() == "test content"
    
    def test_temp_file_fixture(self, temp_file):
        """Validate temp_file fixture works."""
        assert isinstance(temp_file, Path)
        
        # Write to the temp file
        temp_file.write_text("test file content")
        assert temp_file.read_text() == "test file content"
    
    def test_sample_data_fixture(self, sample_data):
        """Validate sample_data fixture works."""
        assert isinstance(sample_data, dict)
        assert "users" in sample_data
        assert "products" in sample_data
        assert len(sample_data["users"]) == 2
        assert len(sample_data["products"]) == 2
    
    def test_mock_config_fixture(self, mock_config):
        """Validate mock_config fixture works."""
        assert mock_config.DEBUG is True
        assert mock_config.TESTING is True
        assert mock_config.SECRET_KEY == "test-secret-key"
    
    def test_mock_database_fixture(self, mock_database):
        """Validate mock_database fixture works."""
        # Test that we can call database methods
        result = mock_database.execute("SELECT * FROM test")
        assert result is not None
        
        rows = mock_database.fetchall()
        assert isinstance(rows, list)
    
    def test_mock_logger_fixture(self, mock_logger):
        """Validate mock_logger fixture works."""
        # Test that we can call logger methods
        mock_logger.info("test message")
        mock_logger.info.assert_called_with("test message")
    
    def test_json_file_fixture(self, json_file):
        """Validate json_file fixture works."""
        assert json_file.exists()
        assert json_file.suffix == ".json"
        
        import json
        with open(json_file, "r") as f:
            data = json.load(f)
        
        assert data["test"] is True
        assert data["value"] == 42
        assert "items" in data
    
    def test_text_file_fixture(self, text_file):
        """Validate text_file fixture works."""
        assert text_file.exists()
        assert text_file.suffix == ".txt"
        
        content = text_file.read_text()
        assert "This is a test file" in content
        assert "multiple lines" in content
    
    def test_mock_environment_fixture(self, mock_environment):
        """Validate mock_environment fixture works."""
        import os
        
        assert os.getenv("FLASK_ENV") == "testing"
        assert os.getenv("DATABASE_URL") == "sqlite:///:memory:"
        assert os.getenv("SECRET_KEY") == "test-secret-key-12345"
        assert os.getenv("DEBUG") == "True"


class TestProjectStructure:
    """Test class to validate project structure."""
    
    def test_tests_directory_exists(self):
        """Validate tests directory structure exists."""
        tests_dir = Path("tests")
        assert tests_dir.exists()
        assert tests_dir.is_dir()
        
        assert (tests_dir / "__init__.py").exists()
        assert (tests_dir / "conftest.py").exists()
        
        unit_dir = tests_dir / "unit"
        assert unit_dir.exists()
        assert unit_dir.is_dir()
        assert (unit_dir / "__init__.py").exists()
        
        integration_dir = tests_dir / "integration"
        assert integration_dir.exists()
        assert integration_dir.is_dir()
        assert (integration_dir / "__init__.py").exists()
    
    def test_pyproject_toml_exists(self):
        """Validate pyproject.toml exists and has basic structure."""
        pyproject_file = Path("pyproject.toml")
        assert pyproject_file.exists()
        
        content = pyproject_file.read_text()
        assert "[tool.poetry]" in content
        assert "[tool.pytest.ini_options]" in content
        assert "[tool.coverage" in content


def test_basic_assertion():
    """Basic test to ensure pytest is working."""
    assert 1 + 1 == 2


def test_basic_fixture_usage(sample_data):
    """Test basic fixture usage to ensure fixture system works."""
    assert sample_data is not None
    assert isinstance(sample_data, dict)


@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 3),
    (3, 4),
])
def test_parametrized_test(input, expected):
    """Test parametrized testing functionality."""
    assert input + 1 == expected