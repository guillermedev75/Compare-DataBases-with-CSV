IF OBJECT_ID('tempdb..#TempTableInfo') IS NOT NULL
BEGIN
    DROP TABLE #TempTableInfo;
END

CREATE TABLE #TempTableInfo (
    DatabaseName NVARCHAR(128),
    TABLE_SCHEMA NVARCHAR(128),
    TABLE_NAME NVARCHAR(128),
    RecordCount BIGINT
);

DECLARE @DatabaseName NVARCHAR(128);
DECLARE @SQL NVARCHAR(MAX);

DECLARE db_cursor CURSOR FOR
SELECT name
FROM sys.databases
WHERE state_desc = 'ONLINE' AND database_id > 4 -- Exclui bases de sistema como master, tempdb, etc.

OPEN db_cursor;
FETCH NEXT FROM db_cursor INTO @DatabaseName;

WHILE @@FETCH_STATUS = 0
BEGIN
    SET @SQL = '
    INSERT INTO #TempTableInfo (DatabaseName, TABLE_SCHEMA, TABLE_NAME, RecordCount)
    SELECT 
        ''' + @DatabaseName + ''', 
        TABLE_SCHEMA,
        TABLE_NAME, 
        SUM(PARTITIONS.rows) AS RecordCount
    FROM 
        ' + QUOTENAME(@DatabaseName) + '.INFORMATION_SCHEMA.TABLES AS T
    INNER JOIN 
        ' + QUOTENAME(@DatabaseName) + '.sys.tables AS ST ON T.TABLE_NAME = ST.name
    INNER JOIN 
        ' + QUOTENAME(@DatabaseName) + '.sys.partitions AS PARTITIONS ON ST.object_id = PARTITIONS.object_id
    WHERE 
        PARTITIONS.index_id IN (0, 1) -- Considerar apenas as partições de índice de heap e clusterizado
    GROUP BY 
        TABLE_SCHEMA,
        TABLE_NAME;';

    EXEC sp_executesql @SQL;

    FETCH NEXT FROM db_cursor INTO @DatabaseName;
END;

CLOSE db_cursor;
DEALLOCATE db_cursor;

SELECT * 
FROM #TempTableInfo 
ORDER BY DatabaseName, RecordCount DESC;