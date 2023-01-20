from pgConstants import PG_TABLE, PG_VIEW, PG_MATERIALIZED_VIEW, PG_UNKNOWN

CATALOG_COUNT_QUERY = "SELECT COUNT(*) FROM %s WHERE schemaname = %s and tablename = %s"


def _isA(conn, schemaName: str, tableName: str, catalogName: str):
    xaction = conn.cursor()
    xaction.execute(CATALOG_COUNT_QUERY, (catalogName, schemaName, tableName))
    response = xaction.fetchone()
    xaction.close()
    return response[0] > 0


def isTable(conn, schemaName: str, tableName: str):
    return _isA(conn, schemaName, tableName, catalogName=PG_TABLE)


def isView(conn, schemaName: str, tableName: str):
    return _isA(conn, schemaName, tableName, catalogName=PG_VIEW)


def isMaterializedView(conn, schemaName: str, tableName: str):
    return _isA(conn, schemaName, tableName, catalogName=PG_MATERIALIZED_VIEW)


def getCatalogType(conn, schemaName: str, tableName: str):
    if isTable(conn, schemaName, tableName):
        return PG_TABLE
    elif isView(conn, schemaName, tableName):
        return PG_VIEW
    elif isMaterializedView(conn, schemaName, tableName):
        return PG_MATERIALIZED_VIEW
    else:
        return PG_UNKNOWN
