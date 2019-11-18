def pytest_configure(config):
    # Emulates the loading of the app
    from django_ltree.apps import register_pathfield

    register_pathfield()
