_getPrimaryKeyColumnSql = """
SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
FROM   pg_index i
JOIN   pg_attribute a ON a.attrelid = i.indrelid
                     AND a.attnum = ANY(i.indkey)
WHERE  i.indrelid = '{}.{}'::regclass
AND    i.indisprimary;
"""


def getPrimaryKeyNamesAndTypes(conn, schemaName: str, tableName: str):
    """returns a dict with the primary key column names as keys, the data type are the values, ie: {'id':'integer'}"""
    xaction = conn.cursor()
    xaction.execute(_getPrimaryKeyColumnSql.format(schemaName, tableName))
    response = xaction.fetchall()
    pks = {}
    for r in response:
        pks[r[0]] = r[1]
    xaction.close()
    return pks
