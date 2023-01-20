from kissom.utils.storeConfig import createColumnDict
from kissom.appExceptions import CatalogNameDoesNotExistException

_SELECT_VIEW_SCHEMA_SQL = """
SELECT
  a.attnum,
  a.attname,
  pg_catalog.format_type(a.atttypid, a.atttypmod),
  a.attnotnull
FROM pg_attribute a
  JOIN pg_class t on a.attrelid = t.oid
  JOIN pg_namespace s on t.relnamespace = s.oid
WHERE a.attnum > 0 
  AND NOT a.attisdropped
  AND t.relname = %s
  AND s.nspname = %s
ORDER BY a.attnum;
"""


def getViewInfo(conn, schemaName: str, viewName: str,raiseExceptionIfNoData:bool=True):
    xaction = conn.cursor()
    xaction.execute(_SELECT_VIEW_SCHEMA_SQL, (viewName, schemaName))
    response = xaction.fetchall()
    viewData = []
    for r in response:
        column = createColumnDict(
            index=r[0], name=r[1], type=r[2].lower(), default=None, isNullable=True, isUpdatable=False
        )
        viewData.append(column)
    xaction.close()
    if raiseExceptionIfNoData and not viewData:
        raise CatalogNameDoesNotExistException(tablename=viewName)
    return viewData
