import time
from contextlib import contextmanager

from django.db.backends.mysql.base import DatabaseWrapper as DjangoDatabaseWrapper
from django.db.backends.utils import CursorWrapper as DjangoCursorWrapper


@contextmanager
def calc_sql_time(sql):
    timestamp = time.monotonic()
    yield
    print(
        f'Продолжительность SQL-запроса {sql} - '
        f'{time.monotonic() - timestamp:.3f} сек.'
    )

class CursorWrapper(DjangoCursorWrapper):
    def execute(self, sql, params=None):
        print('khjkvbjv')
        with calc_sql_time(sql):
            return super().execute(sql, params or ())

class DatabaseWrapper(DjangoDatabaseWrapper):
    def create_cursor(self, name=None):
        print('dfgrgr')
        cursor = super().create_cursor(name)
        return CursorWrapper(cursor, self)
