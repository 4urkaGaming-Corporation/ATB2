-- Проверка и создание пользователя, если он не существует
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'store_user') THEN
        CREATE USER store_user WITH PASSWORD 'store_password';
        ALTER USER store_user CREATEDB;
    END IF;
END
$$;

-- Подключение к базе данных store (она уже создана через POSTGRES_DB)
\c store

-- Предоставление привилегий на базу данных
GRANT ALL PRIVILEGES ON DATABASE store TO store_user;

-- Предоставление прав на схему public
GRANT USAGE ON SCHEMA public TO store_user;

-- Предоставление прав на все существующие таблицы и последовательности
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO store_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO store_user;

-- Установка прав по умолчанию для будущих таблиц и последовательностей
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO store_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO store_user;