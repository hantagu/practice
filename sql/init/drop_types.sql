DO $$
DECLARE
    i RECORD;
BEGIN
    FOR i IN (SELECT "typname" from "pg_catalog"."pg_type" where "typtype" = 'e')
    LOOP
        EXECUTE 'DROP TYPE ' || i.typname;
    END LOOP;
END;
$$;
