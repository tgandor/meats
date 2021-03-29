declare userSchemas cursor for
SELECT name
FROM sys.schemas
WHERE schema_id > schema_id('sys');
declare @schemaName varchar(255);
declare @strSQL varchar(max);
open userSchemas;

Fetch Next FROM userSchemas into @schemaName;
print @schemaName;

While @@FETCH_STATUS=0 Begin;
    SET @strSQL='grant select, update, insert, delete, execute
                 ON schema::[' + @schemaName + '] to public;'
    exec sp_sqlexec @strSQL;
    FETCH NEXT FROM userSchemas INTO @schemaName;
    print @schemaName;
END;
Close userSchemas;
Deallocate userSchemas;
