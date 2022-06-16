#!/usr/bin/env python3
from postgres_db import PostgresService


table = PostgresService(
    user = 'postgres',
    password = 'postgres',
    host = '127.0.0.1',
    port = '5432',
    dbname = 'falcondb',
    table = 'strongbox.sb_email',
    primarykey = 'email'
)


table.connect()


table.insert(
    email = 'test@test.com',
    source_table = 'zb'
)


table.insert_many(
    columns = ('email', 'source_table'),
    rows = [
        ['test2@test.com', 'zb'],
        ['test3@test.com', 'ci']
    ]
)


table.commit()


table.select_all()


table.select_all(
    primaryKey_value = 'test@test.com'
)


table.select(
    columns = ['source_table'],
    primaryKey_value = 'test@test.com'
)


table.select(
    columns = ['source_table']
)


table.update(
    column = 'source_table',
    column_value = 'zb',
    primaryKey_value = 'test3@test.com'
)


table.update_multiple_columns(
    columns = ['email', 'source_table'],
    columns_value = ['testtest@test.com', 'ci'],
    primaryKey_value = 'test@test.com'
)


table.delete(
    primaryKey_value = 'test@test.com'
)


table.select_all()


table.delete_all()


table.close("commit")

