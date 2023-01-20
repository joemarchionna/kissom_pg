from kissom.appExceptions import CatalogNameDoesNotExistException
from kissom.utils.names import combineFQTN
from kissom.utils.storeConfig import createColumnDict
from kissom_pg.pgCmds.pgPrimaryKeyInfo import getPrimaryKeyNamesAndTypes


_SELECT_INFO_SQL = """
SELECT ordinal_position, column_name, data_type, column_default, is_nullable, is_updatable 
FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s 
ORDER BY ordinal_position
"""


def getTableInfo(conn, schemaName: str, tableName: str, includePrimaryKeyInfo: bool = False):
    """returns a list of dicts, one for each column in the table specified, with primary key information merged"""
    tableColumns = _getTableInfo(conn, schemaName, tableName)
    if not includePrimaryKeyInfo:
        return tableColumns
    primaryKeys = getPrimaryKeyNamesAndTypes(conn, schemaName, tableName)
    for column in tableColumns:
        column["isPrimaryKey"] = column["name"] in primaryKeys
    return tableColumns


def _getTableInfo(conn, schemaName: str, tableName: str, raiseExceptionIfNoData:bool=True):
    xaction = conn.cursor()
    xaction.execute(_SELECT_INFO_SQL, (schemaName, tableName))
    response = xaction.fetchall()
    tableData = []
    for r in response:
        column = createColumnDict(
            index=r[0],
            name=r[1],
            type=r[2].lower(),
            default=r[3],
            isNullable=(r[4] == "YES"),
            isUpdatable=(r[5] == "YES"),
        )
        tableData.append(column)
    xaction.close()
    if raiseExceptionIfNoData and not tableData:
        raise CatalogNameDoesNotExistException(tablename=combineFQTN(schemaName=schemaName, tableName=tableName))
    return tableData
