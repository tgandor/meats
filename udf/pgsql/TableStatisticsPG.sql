-- Reference: https://stackoverflow.com/questions/18907047/postgres-db-size-command

create or replace function
cnt_rows(schema text, tablename text) returns integer as
$body$
declare
    result integer;
    query varchar;
begin
    query := 'SELECT count(1) FROM ' || schema || '.' || tablename;
    execute query into result;
    return result;
end;
$body$
language plpgsql;

select
    table_schema,
    table_name,
    cnt_rows(table_schema, table_name) as num_rows,
    pg_size_pretty(pg_total_relation_size(table_schema || '.' || table_name)) as total_size,
    pg_size_pretty(pg_relation_size(table_schema || '.' || table_name)) as relation_size
from information_schema.tables
where
    table_schema not in ('pg_catalog', 'information_schema')
    and table_type='BASE TABLE' order by 3 desc;
