from kissom.storeAdapter import StoreAdapter
from kissom.utils.names import splitFQTN
from kissom.utils.mapping import getDictFromTuple
from kissom.utils.sql import insertSql, selectSql, updateSql, deleteSql
from kissom_pg.pgCmds.pgTableInfo import getTableInfo
import psycopg2


class PgAdapter(StoreAdapter):
    def __init__(
        self,
        logName: str = None,
        connectionString: str = "host=localhost dbname=databaseName user=databaseUser password=password123",
        openConnection: bool = True,
    ):
        super().__init__(logName=logName)
        self.connStr = connectionString
        self.connection = None
        if openConnection:
            self.connection = self.openConnection()

    def openConnection(self):
        self.logger.debug("Opening Connection")
        return psycopg2.connect(self.connStr)

    def closeConnection(self):
        if self.connection and (self.connection.closed == False):
            self.connection.close()

    def getTransactionCursor(self):
        return self.connection.cursor()

    def getTableDefinition(self, tableName: str):
        sName, tName = splitFQTN(fullyQualifiedTableName=tableName)
        columnList = getTableInfo(conn=self.connection, schemaName=sName, tableName=tName, includePrimaryKeyInfo=True)
        return columnList

    def insert(self, fqtn: str, dbKeys: list, objKeys: list, obj: dict, xaction=None):
        _sql, _values = insertSql(tableName=fqtn, objKeys=objKeys, dbKeys=dbKeys, data=obj)
        _values = self._execute(sql=_sql, values=_values, xaction=xaction, commitXaction=True)
        _records = self._getRecords(values=_values, objKeys=objKeys)
        if _records and len(_records) == 1:
            return _records[0]
        return _records

    def select(self, fqtn: str, dbKeys: list, objKeys: list, conditions: dict):
        _sql, _values = selectSql(tableName=fqtn, dbKeys=dbKeys, conditionTree=conditions)
        _values = self._execute(sql=_sql, values=_values)
        return self._getRecords(values=_values, objKeys=objKeys)

    def update(self, fqtn: str, dbKeys: list, objKeys: list, obj: dict, conditions: dict, xaction=None):
        _sql, _values = updateSql(tableName=fqtn, objKeys=objKeys, dbKeys=dbKeys, data=obj, conditionTree=conditions)
        _values = self._execute(sql=_sql, values=_values, xaction=xaction, commitXaction=True)
        return self._getRecords(values=_values, objKeys=objKeys)

    def delete(self, fqtn: str, dbKeys: list, objKeys: list, conditions: dict, xaction=None):
        _sql, _values = deleteSql(tableName=fqtn, dbKeys=dbKeys, conditionTree=conditions)
        _values = self._execute(sql=_sql, values=_values, xaction=xaction, commitXaction=True)
        return self._getRecords(values=_values, objKeys=objKeys)

    def _execute(self, sql: str, values: tuple, xaction=None, commitXaction: bool = False):
        _close = False
        if not xaction:
            xaction = self.connection.cursor()
            _close = True
        xaction.execute(sql, values)
        _records = xaction.fetchall()
        if _close:
            if commitXaction:
                self.connection.commit()
            xaction.close()
        return _records

    def _getRecords(self, values: list, objKeys: list):
        _objects = []
        for v in values:
            _objects.append(getDictFromTuple(values=v, keys=objKeys))
        return _objects