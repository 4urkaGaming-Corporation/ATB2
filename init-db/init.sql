CREATE USER store_user WITH PASSWORD 'store_password';
ALTER USER store_user CREATEDB; 
GRANT ALL PRIVILEGES ON DATABASE store TO store_user;