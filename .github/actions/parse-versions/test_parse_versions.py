#!/usr/bin/env python3
"""
Unit tests for parse_versions.py
"""

import pytest
import tempfile
import os
from pathlib import Path
from parse_versions import parse_toml, set_output


@pytest.fixture
def temp_toml_file():
    """Create a temporary TOML file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write("""
[versions]
python-ci = "3.11"
java-ci = "17"
java-toolchain = "17"
java-target = "11"
kotlin = "2.3.0"
agp = "8.13.0"
""")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def minimal_toml_file():
    """Create a minimal TOML file with only required versions."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write("""
[versions]
java-ci = "21"
python-ci = "3.12"
""")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def empty_toml_file():
    """Create an empty TOML file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write("[versions]\n")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


class TestParseToml:
    """Tests for parse_toml function."""
    
    def test_parse_valid_toml(self, temp_toml_file):
        """Test parsing a valid TOML file."""
        data = parse_toml(temp_toml_file)
        
        assert 'versions' in data
        assert data['versions']['java-ci'] == '17'
        assert data['versions']['python-ci'] == '3.11'
        assert data['versions']['kotlin'] == '2.3.0'
    
    def test_parse_minimal_toml(self, minimal_toml_file):
        """Test parsing a minimal TOML file."""
        data = parse_toml(minimal_toml_file)
        
        assert 'versions' in data
        assert data['versions']['java-ci'] == '21'
        assert data['versions']['python-ci'] == '3.12'
    
    def test_parse_empty_versions(self, empty_toml_file):
        """Test parsing TOML with empty versions section."""
        data = parse_toml(empty_toml_file)
        
        assert 'versions' in data
        assert data['versions'] == {}
    
    def test_parse_nonexistent_file(self):
        """Test parsing a non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            parse_toml('nonexistent.toml')


class TestVersionExtraction:
    """Tests for version extraction logic."""
    
    def test_extract_all_versions(self, temp_toml_file):
        """Test extracting all versions from TOML."""
        data = parse_toml(temp_toml_file)
        versions = data.get('versions', {})
        
        java_ci = versions.get('java-ci', '17')
        python_ci = versions.get('python-ci', '3.11')
        
        assert java_ci == '17'
        assert python_ci == '3.11'
    
    def test_extract_with_defaults(self, empty_toml_file):
        """Test that defaults are used when versions are missing."""
        data = parse_toml(empty_toml_file)
        versions = data.get('versions', {})
        
        java_ci = versions.get('java-ci', '17')
        python_ci = versions.get('python-ci', '3.11')
        
        # Should use defaults
        assert java_ci == '17'
        assert python_ci == '3.11'
    
    def test_extract_custom_versions(self, minimal_toml_file):
        """Test extracting custom version values."""
        data = parse_toml(minimal_toml_file)
        versions = data.get('versions', {})
        
        java_ci = versions.get('java-ci', '17')
        python_ci = versions.get('python-ci', '3.11')
        
        # Should use custom values, not defaults
        assert java_ci == '21'
        assert python_ci == '3.12'


class TestSetOutput:
    """Tests for set_output function."""
    
    def test_set_output_format(self, capsys):
        """Test that set_output produces correct GitHub Actions format."""
        set_output('test-key', 'test-value')
        
        captured = capsys.readouterr()
        assert '::set-output name=test-key::test-value' in captured.out
    
    def test_set_output_multiple(self, capsys):
        """Test setting multiple outputs."""
        set_output('key1', 'value1')
        set_output('key2', 'value2')
        
        captured = capsys.readouterr()
        assert '::set-output name=key1::value1' in captured.out
        assert '::set-output name=key2::value2' in captured.out


class TestIntegration:
    """Integration tests for the full parsing flow."""
    
    def test_full_parse_flow(self, temp_toml_file, capsys):
        """Test the complete parsing flow."""
        data = parse_toml(temp_toml_file)
        versions = data.get('versions', {})
        
        java_ci = versions.get('java-ci', '17')
        python_ci = versions.get('python-ci', '3.11')
        
        set_output('java-version', java_ci)
        set_output('python-version', python_ci)
        
        captured = capsys.readouterr()
        assert '::set-output name=java-version::17' in captured.out
        assert '::set-output name=python-version::3.11' in captured.out
    
    def test_parse_with_missing_versions(self, empty_toml_file, capsys):
        """Test parsing when versions are missing (should use defaults)."""
        data = parse_toml(empty_toml_file)
        versions = data.get('versions', {})
        
        java_ci = versions.get('java-ci', '17')
        python_ci = versions.get('python-ci', '3.11')
        
        set_output('java-version', java_ci)
        set_output('python-version', python_ci)
        
        captured = capsys.readouterr()
        # Should output defaults
        assert '::set-output name=java-version::17' in captured.out
        assert '::set-output name=python-version::3.11' in captured.out


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
