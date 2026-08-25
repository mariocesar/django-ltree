from django.db import connections
from django.db import router as db_router

from django_ltree.checks import check_database_is_supported_postgres


class DenyLtreeRouter:
    def allow_migrate(self, db, app_label, **hints):
        return app_label != "django_ltree"


def test_current_database_passes(db):
    assert check_database_is_supported_postgres(None, databases=["default"]) == []


def test_old_postgres_fails(db, monkeypatch):
    connection = connections["default"]
    monkeypatch.setattr(connection, "pg_version", 150004, raising=False)

    errors = check_database_is_supported_postgres(None, databases=["default"])

    assert [error.id for error in errors] == ["django_ltree.E001"]
    assert "PostgreSQL 15" in errors[0].msg


def test_non_postgres_connection_fails(db, monkeypatch):
    connection = connections["default"]
    monkeypatch.setattr(type(connection), "vendor", "sqlite")

    errors = check_database_is_supported_postgres(None, databases=["default"])

    assert [error.id for error in errors] == ["django_ltree.E002"]
    assert "'sqlite'" in errors[0].msg


def test_router_excluded_database_is_skipped(db, monkeypatch):
    connection = connections["default"]
    monkeypatch.setattr(type(connection), "vendor", "sqlite")
    monkeypatch.setattr(db_router, "routers", [DenyLtreeRouter()])

    assert check_database_is_supported_postgres(None, databases=["default"]) == []


def test_no_databases_given():
    assert check_database_is_supported_postgres(None, databases=None) == []
