from django.db import migrations


def protect(apps, schema_editor):
    connection = schema_editor.connection
    if connection.vendor != 'postgresql':
        return
    names = {m._meta.db_table for m in apps.get_models()}
    names.add('django_migrations')
    with connection.cursor() as cursor:
        cursor.execute("SELECT rolname FROM pg_roles WHERE rolname IN ('anon', 'authenticated')")
        roles = [row[0] for row in cursor.fetchall()]
        present = set(connection.introspection.table_names(cursor))
        for name in sorted(names & present):
            table = connection.ops.quote_name(name)
            cursor.execute(f'ALTER TABLE {table} ENABLE ROW LEVEL SECURITY')
            cursor.execute(f'REVOKE ALL ON TABLE {table} FROM PUBLIC')
            for role in roles:
                cursor.execute(f'REVOKE ALL ON TABLE {table} FROM {connection.ops.quote_name(role)}')


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial'), ('sessions', '0001_initial'), ('auth', '0012_alter_user_first_name_max_length')]
    operations = [migrations.RunPython(protect, migrations.RunPython.noop)]
