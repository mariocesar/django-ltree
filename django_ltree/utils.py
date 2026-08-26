from django.db import DEFAULT_DB_ALIAS, connections


def pad_path_labels(model, label_width: int, using: str = DEFAULT_DB_ALIAS) -> int:
    """
    Zero-pad every numeric label in `model`'s paths to `label_width`.

    Use this in a data migration when enabling `TreeManager(label_width=...)`
    on a model that already has data:

        def forwards(apps, schema_editor):
            pad_path_labels(
                apps.get_model("myapp", "Category"),
                label_width=10,
                using=schema_editor.connection.alias,
            )

    Non-numeric labels, and numeric labels already wider than `label_width`,
    are left untouched. Returns the number of rows updated.
    """
    connection = connections[using]
    quote = connection.ops.quote_name
    table = quote(model._meta.db_table)
    path = quote(model._meta.get_field("path").column)

    # Identifiers come from model metadata quoted with quote_name, and
    # values are passed as query parameters.
    query = (  # noqa: S608
        "UPDATE {table} SET {path} = text2ltree("
        " (SELECT string_agg("
        "         CASE WHEN t.label ~ '^[0-9]+$' AND char_length(t.label) <= %s"
        "              THEN lpad(t.label, %s, '0')"
        "              ELSE t.label END,"
        "         '.' ORDER BY t.pos)"
        "  FROM unnest(string_to_array(ltree2text({path}), '.'))"
        "       WITH ORDINALITY AS t(label, pos))"
        ") WHERE {path} IS NOT NULL"
    ).format(table=table, path=path)

    with connection.cursor() as cursor:
        cursor.execute(query, [label_width, label_width])
        return cursor.rowcount
