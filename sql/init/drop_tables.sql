DO $$
DECLARE
    i RECORD;
BEGIN
    FOR i IN (SELECT "table_name" FROM "information_schema"."tables" WHERE "table_schema" = 'public')
    LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || i.table_name || ' CASCADE';
    END LOOP;
END;
$$;
