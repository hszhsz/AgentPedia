import os
import pytest

try:
    from agentpedia.core.config import Settings, TestingSettings
except Exception:
    pytest.skip("后端依赖未安装，跳过配置相关测试", allow_module_level=True)


def test_get_cors_origins_empty():
    s = Settings()
    s.BACKEND_CORS_ORIGINS = ""
    assert s.get_cors_origins() == []


def test_get_cors_origins_parses_list():
    s = Settings()
    s.BACKEND_CORS_ORIGINS = "http://a.com, https://b.com , http://c.com"
    assert s.get_cors_origins() == [
        "http://a.com",
        "https://b.com",
        "http://c.com",
    ]


def test_get_database_uri_default_postgres():
    s = Settings()
    s.SQLALCHEMY_DATABASE_URI = None
    uri = s.get_database_uri()
    assert uri.startswith("postgresql://")


def test_get_database_uri_override_sqlite():
    s = Settings()
    s.SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
    assert s.get_database_uri() == "sqlite:///./test.db"


def test_get_allowed_extensions_parsed():
    s = Settings()
    s.ALLOWED_EXTENSIONS = ".txt, .md,.json , .yaml,.yml"
    assert s.get_allowed_extensions() == [
        ".txt",
        ".md",
        ".json",
        ".yaml",
        ".yml",
    ]


def test_testing_settings_env_values():
    ts = TestingSettings()
    assert ts.TESTING is True
    assert ts.ENVIRONMENT == "testing"