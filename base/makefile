base:
	sudo -u postgres psql
	CREATE ROLE dengue_bot LOGIN password 'd3ngu3_80t';
	CREATE DATABASE dengue;
	GRANT ALL PRIVILEGES ON DATABASE dengue TO dengue_bot;
	ALTER DATABASE dengue owner to dengue_bot;
	ALTER USER dengue_bot WITH SUPERUSER;
	\q
	psql --username=dengue_bot --host=127.0.0.1 dengue < esquema/dump.sql
	psql dengue --username=dengue_bot --host=127.0.0.1

clean:
	sudo -u postgresql psql
	drop database dengue;
	drop role dengue_bot;

prueba:
	echo hola!
