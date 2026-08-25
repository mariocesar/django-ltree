# Contributing to django-ltree

Thanks for your interest in contributing! Bug reports, fixes, and improvements
are all welcome. For large changes, please open an
[issue](https://github.com/mariocesar/django-ltree/issues) first to discuss.

## Development Requirements

- [uv](https://docs.astral.sh/uv/)
- [Docker](https://docs.docker.com/get-docker/)
- `make`

Tests run entirely inside Docker containers on an internal network, with an ephemeral (tmpfs) database that is recreated on every run.

## Setup

```bash
git clone https://github.com/mariocesar/django-ltree.git
cd django-ltree
make test
```

That's it, Docker pulls the images on first run, starts PostgreSQL and runs the suite.

### Testing against other versions


```bash
make test POSTGRES_VERSION=17
make test POSTGRES_VERSION=latest PYTHON_VERSION=3.11
make test-matrix                     # postgres 16, 17, and latest
```

### Passing pytest arguments

Override the container command to run a subset or add flags:

```bash
docker compose run --rm tests uv run pytest tests/test_path_field.py -x
```

### Inspecting the database

Use `psql` inside the container:

```bash
docker compose up -d postgres
docker compose exec postgres psql -U postgres taxonomy_db
```

Remember the data dir is tmpfs — everything vanishes when the container stops.

## Linting

```bash
make lint                    # ruff check --fix
uvx prek run --all-files     # all pre-commit hooks
```

## Project layout

```
django_ltree/     The app: fields, lookups, managers, models, migrations
tests/conf/       Django settings/urls used by the test suite
tests/taxonomy/   Sample app with tree models the tests run against
tests/            The test suite
```

## Submitting changes

1. Create a branch and make your change. Add or update tests — anything that
   touches path/tree behavior should show up in `tests/`.
2. Run `make lint` and `make test` (ideally `make test-matrix`).
3. Open a pull request against `main`.

CI runs the suite on Python 3.11–3.14 × Django 5.2/6.0 × PostgreSQL
16/latest, so keep changes compatible across that grid.

## Cleaning up

```bash
make clean    # removes python build artifacts, containers, and docker volumes
```
