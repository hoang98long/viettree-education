-- Run as the migration owner after import/restore and after each migration.
-- The application role has no schema CREATE or table ownership.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM viettree_app;
GRANT USAGE ON SCHEMA public TO viettree_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO viettree_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO viettree_app;
ALTER DEFAULT PRIVILEGES FOR ROLE viettree_owner IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO viettree_app;
ALTER DEFAULT PRIVILEGES FOR ROLE viettree_owner IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO viettree_app;
