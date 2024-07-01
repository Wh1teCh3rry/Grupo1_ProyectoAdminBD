--CREACIÓN DE ROLES
-- Crear rol para lectura
CREATE ROLE lectura_grp1;
-- Crear rol para inserción
CREATE ROLE insercion_grp1;
-- Crear rol para inserción, eliminación, actualización y lectura
CREATE ROLE super_grp1;

-----LECTURA
-- Otorgar permisos de lectura a todas las tablas
GRANT SELECT ON ALL TABLES IN SCHEMA public TO lectura_grp1; 
-- Asegurarse de que cualquier tabla nueva creada también otorgue permisos de lectura automáticamente
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO lectura_grp1;

--INSERCIÓN
-- Otorgar permisos de inserción a todas las tablas existentes
GRANT INSERT, SELECT, UPDATE ON ALL TABLES IN SCHEMA public TO insercion_grp1;
-- Asegurarse de que cualquier tabla nueva creada también otorgue permisos de inserción automáticamente
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, SELECT, UPDATE ON TABLES TO insercion_grp1;

--SUPER
-- Otorgar permisos de inserción y eliminación a todas las tablas existentes
GRANT TRUNCATE, INSERT, DELETE, SELECT, UPDATE, TRIGGER ON ALL TABLES IN SCHEMA public TO super_grp1;
-- Asegurarse de que cualquier tabla nueva creada también otorgue permisos de inserción y eliminación automáticamente
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT TRUNCATE, INSERT, DELETE, SELECT, UPDATE, TRIGGER ON TABLES TO super_grp1;

---CREACION USUARIOS
-- Crear usuario analisisbd_grp1
CREATE USER analisisbd_grp1 WITH PASSWORD 'administraciongrupo1accl';
-- Crear usuario arq_grp1
CREATE USER arq_grp1 WITH PASSWORD 'administraciongrupo1accl';
-- Crear usuario dba_grp1
CREATE USER dba_grp1 WITH PASSWORD 'administraciongrupo1accl';

--ASIGNACIÓN DE ROLES
 -- Asignar el rol de lectura a un usuario
GRANT lectura_grp1 TO analisisbd_grp1;
-- Asignar el rol de insercción a un usuario
GRANT insercion_grp1 TO arq_grp1;
-- Asignar el rol de insercción y eliminación a otro usuario
GRANT super_grp1 TO dba_grp1;