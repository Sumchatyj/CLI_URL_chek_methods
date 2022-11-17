import json
import subprocess

import pytest

from cli import validate_url


@pytest.fixture
def script():
    return ["python3", "cli.py"]


def test_validate_url():
    fixtures_good = [
        "http://www.foufos.gr",
        "https://www.foufos.gr",
        "http://foufos.gr",
        "http://www.foufos.gr/kino",
        "http://werer.gr",
        "http://t.co",
        "http://www.t.co",
        "https://www.t.co",
        "http://aa.com",
        "http://www.aa.com",
        "https://www.aa.com",
    ]
    fixtures_bad = [
        "www.foufos.gr",
        "www.foufos-.gr",
        "www.-foufos.gr",
        "foufos.gr",
        "www.mp3#.com",
    ]
    for fixture in fixtures_good:
        assert validate_url(0, fixture) is True
    for fixture in fixtures_bad:
        assert validate_url(0, fixture) is False


def test_one_url(script):
    script.append("https://google.com")
    expected = {"https://google.com": {"GET": 200, "HEAD": 301}}
    expected_json = json.dumps(expected, indent=4)
    result = subprocess.run(script, capture_output=True)
    assert expected_json == result.stdout.decode().strip()


def test_one_wrong_url(script):
    script.append("https://goiyigyfudhlkhiogle.com")
    expected = {"https://goiyigyfudhlkhiogle.com": "try another url"}
    expected_json = json.dumps(expected, indent=4)
    result = subprocess.run(script, capture_output=True)
    assert expected_json == result.stdout.decode().strip()


def test_multiple_url(script):
    urls = ["https://google.com", "https://www.facebook.com"]
    script.extend(urls)
    expected = {
        "https://google.com": {"GET": 200, "HEAD": 301},
        "https://www.facebook.com": {
            "GET": 200,
            "HEAD": 200,
            "OPTIONS": 200,
            "POST": 200,
            "PUT": 200,
            "PATCH": 200,
            "DELETE": 200,
        },
    }
    expected_json = json.dumps(expected, indent=4)
    result = subprocess.run(script, capture_output=True)
    assert expected_json == result.stdout.decode().strip()


def test_broken_url(script):
    script.append("google.com")
    expected = "the string 0 is not a valid URL"
    result = subprocess.run(script, capture_output=True)
    assert expected == result.stdout.decode().strip()


def test_multiple_url_with_broken_url(script):
    urls = ["https://google.com", "google.com", "https://www.facebook.com"]
    script.extend(urls)
    expected_error = "the string 1 is not a valid URL\n"
    expected = {
        "https://google.com": {"GET": 200, "HEAD": 301},
        "https://www.facebook.com": {
            "GET": 200,
            "HEAD": 200,
            "OPTIONS": 200,
            "POST": 200,
            "PUT": 200,
            "PATCH": 200,
            "DELETE": 200,
        },
    }
    expected_json = json.dumps(expected, indent=4)
    expected_result = expected_error + expected_json
    result = subprocess.run(script, capture_output=True)
    assert expected_result == result.stdout.decode().strip()
