from kissom_pg.pgCmds.pgTableInfo import getTableInfo
from kissom_pg.pgCmds.pgViewInfo import getViewInfo
from kissom_pg.pgCmds.pgTypeInfo import isTable


def getCatalogInfo(conn, schemaName: str, tableName: str, includePrimaryKeyInfo: bool = False):
    if isTable(conn=conn, schemaName=schemaName, tableName=tableName):
        return {
            "isTable": True,
            "columns": getTableInfo(
                conn=conn, schemaName=schemaName, tableName=tableName, includePrimaryKeyInfo=includePrimaryKeyInfo
            ),
        }
    return {"isTable": False, "columns": getViewInfo(conn=conn, schemaName=schemaName, viewName=tableName)}
