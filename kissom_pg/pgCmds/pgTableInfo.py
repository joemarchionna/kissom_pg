from kissom.appExceptions import TableNameDoesNotExistException
from kissom_pg.pgCmds.pgPrimaryKeyInfo import getPrimaryKeyNamesAndTypes


_selectInfoSchemaSql = """SELECT ordinal_position, column_name, data_type, column_default, is_nullable, is_updatable FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'"""


def getTableInfo(conn, schemaName: str, tableName: str, includePrimaryKeyInfo: bool = False):
    """returns a list of dicts, one for each column in the table specified"""
    """returns a list of dicts, one for each column in the table specified, with primary key information merged"""
    tableColumns = _getTableInfo(conn, schemaName, tableName)
    if not includePrimaryKeyInfo:
        return tableColumns
    primaryKeys = getPrimaryKeyNamesAndTypes(conn, schemaName, tableName)
    for column in tableColumns:
        column["isPrimaryKey"] = column["name"] in primaryKeys
    return tableColumns


def _getTableInfo(conn, schemaName: str, tableName: str, includePrimaryKeyInfo: bool = False):
    xaction = conn.cursor()
    xaction.execute(_selectInfoSchemaSql.format(schemaName, tableName))
    response = xaction.fetchall()
    tableData = []
    for r in response:
        tableData.append(
            {
                "index": r[0],
                "name": r[1],
                "type": r[2].lower(),
                "default": r[3],
                "isNullable": (r[4] == "YES"),
                "isUpdatable": (r[5] == "YES"),
            }
        )
    xaction.close()
    if not tableData:
        raise TableNameDoesNotExistException(tablename=tableName)
    tableData.sort(key=lambda x: x.get("index"))
    return tableData
