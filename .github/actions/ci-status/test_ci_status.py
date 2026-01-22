#!/usr/bin/env python3
"""
Tests for CI Status Checker

Run with: pytest test_ci_status.py -v
Coverage: pytest test_ci_status.py --cov=ci_status --cov-report=term-missing
"""

import pytest
import yaml
from pathlib import Path
from ci_status import (
    load_config,
    check_branch_enabled,
    get_current_branch,
    create_annotation,
    format_list,
)


# Fixtures

@pytest.fixture
def sample_config():
    """Sample project configuration"""
    return {
        'ci': {
            'enabled_branches': ['main', 'develop'],
            'runners': {'primary': 'ubuntu-latest'},
            'gradle_flags': ['--parallel', '--configuration-cache'],
            'caching': {'kotlin_native': True}
        },
        'versions': {
            'java': '17',
            'python': '3.11',
            'kotlin': '2.3.0'
        },
        'documentation': {
            'github_pages': {'enabled': False}
        }
    }


@pytest.fixture
def temp_config_file(tmp_path, sample_config):
    """Create a temporary config file"""
    config_file = tmp_path / "project.yml"
    config_file.write_text(yaml.dump(sample_config))
    return config_file


# Test load_config

def test_load_config_success(temp_config_file):
    """Test loading a valid config file"""
    config = load_config(str(temp_config_file))
    assert 'ci' in config
    assert config['ci']['enabled_branches'] == ['main', 'develop']


def test_load_config_missing_file():
    """Test loading a non-existent file raises error"""
    with pytest.raises(FileNotFoundError):
        load_config('nonexistent.yml')


# Test check_branch_enabled

@pytest.mark.parametrize("branch,enabled_branches,expected", [
    # List scenarios
    ('main', ['main'], True),
    ('main', ['main', 'develop'], True),
    ('develop', ['main', 'develop'], True),
    ('feature', ['main', 'develop'], False),
    ('feature/xyz', ['main', 'develop'], False),
    
    # Special values
    ('main', 'all', True),
    ('feature', 'all', True),
    ('anything', 'all', True),
    ('main', False, False),
    ('main', 'false', False),
    
    # Edge cases
    ('main', [], False),
])
def test_check_branch_enabled(branch, enabled_branches, expected):
    """Test branch enabling logic with various scenarios"""
    assert check_branch_enabled(branch, enabled_branches) == expected


def test_check_branch_enabled_case_sensitive():
    """Test that branch checking is case-sensitive"""
    assert check_branch_enabled('main', ['Main']) == False
    assert check_branch_enabled('MAIN', ['main']) == False


# Test get_current_branch

def test_get_current_branch_push(monkeypatch):
    """Test getting branch on push event"""
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'push')
    monkeypatch.setenv('GITHUB_REF_NAME', 'main')
    assert get_current_branch() == 'main'


def test_get_current_branch_pull_request(monkeypatch):
    """Test getting branch on PR event (uses base ref)"""
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'pull_request')
    monkeypatch.setenv('GITHUB_BASE_REF', 'develop')
    monkeypatch.setenv('GITHUB_REF_NAME', 'feature/test')
    assert get_current_branch() == 'develop'


def test_get_current_branch_default(monkeypatch):
    """Test default branch when env vars not set"""
    monkeypatch.delenv('GITHUB_EVENT_NAME', raising=False)
    monkeypatch.delenv('GITHUB_REF_NAME', raising=False)
    assert get_current_branch() == 'main'


# Test create_annotation

def test_create_annotation_warning():
    """Test creating a warning annotation"""
    result = create_annotation('warning', 'CI Skipped', 'Build will be skipped')
    assert result == '::warning title=CI Skipped::Build will be skipped'


def test_create_annotation_notice():
    """Test creating a notice annotation"""
    result = create_annotation('notice', 'CI Enabled', 'Build will run')
    assert result == '::notice title=CI Enabled::Build will run'


def test_create_annotation_error():
    """Test creating an error annotation"""
    result = create_annotation('error', 'Failed', 'Something went wrong')
    assert result == '::error title=Failed::Something went wrong'


# Test format_list

def test_format_list_with_list():
    """Test formatting a list"""
    assert format_list(['a', 'b', 'c']) == 'a,b,c'
    assert format_list([1, 2, 3]) == '1,2,3'
    assert format_list([]) == ''


def test_format_list_with_string():
    """Test formatting a string"""
    assert format_list('test') == 'test'
    assert format_list('all') == 'all'


def test_format_list_with_bool():
    """Test formatting a boolean"""
    assert format_list(True) == 'True'
    assert format_list(False) == 'False'


# Integration tests

def test_full_workflow_ci_enabled(monkeypatch, sample_config):
    """Test full workflow when CI is enabled"""
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'push')
    monkeypatch.setenv('GITHUB_REF_NAME', 'main')
    
    branch = get_current_branch()
    enabled_branches = sample_config['ci']['enabled_branches']
    
    assert branch == 'main'
    assert check_branch_enabled(branch, enabled_branches) == True


def test_full_workflow_ci_disabled(monkeypatch, sample_config):
    """Test full workflow when CI is disabled"""
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'push')
    monkeypatch.setenv('GITHUB_REF_NAME', 'feature/test')
    
    branch = get_current_branch()
    enabled_branches = sample_config['ci']['enabled_branches']
    
    assert branch == 'feature/test'
    assert check_branch_enabled(branch, enabled_branches) == False


def test_full_workflow_pr_to_main(monkeypatch, sample_config):
    """Test PR workflow targeting main branch"""
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'pull_request')
    monkeypatch.setenv('GITHUB_BASE_REF', 'main')
    monkeypatch.setenv('GITHUB_REF_NAME', 'feature/test')
    
    branch = get_current_branch()
    enabled_branches = sample_config['ci']['enabled_branches']
    
    # Should check against base branch (main), not feature branch
    assert branch == 'main'
    assert check_branch_enabled(branch, enabled_branches) == True


def test_config_with_all_branches(monkeypatch):
    """Test configuration with 'all' enabled"""
    config = {'ci': {'enabled_branches': 'all'}}
    
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'push')
    monkeypatch.setenv('GITHUB_REF_NAME', 'random-branch')
    
    branch = get_current_branch()
    enabled_branches = config['ci']['enabled_branches']
    
    assert check_branch_enabled(branch, enabled_branches) == True


def test_config_with_disabled_ci(monkeypatch):
    """Test configuration with CI completely disabled"""
    config = {'ci': {'enabled_branches': False}}
    
    monkeypatch.setenv('GITHUB_EVENT_NAME', 'push')
    monkeypatch.setenv('GITHUB_REF_NAME', 'main')
    
    branch = get_current_branch()
    enabled_branches = config['ci']['enabled_branches']
    
    assert check_branch_enabled(branch, enabled_branches) == False
