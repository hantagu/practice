DO $$
BEGIN
    CREATE TYPE "user_role" AS ENUM ('student', 'teacher', 'curator', 'admin');
EXCEPTION
    WHEN duplicate_object THEN
        NULL;
END;
$$;


DO $$
BEGIN
    CREATE TYPE "scoring_system" AS ENUM ('abstract', 'points');
EXCEPTION
    WHEN duplicate_object THEN
        NULL;
END;
$$;
