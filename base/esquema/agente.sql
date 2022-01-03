create table agente (
	agente_id int primary key,
	nombre varchar(64) not null,
	apellido varchar(64) null,
	latitud float not null,
	longitud float not null,
	fecha TIMESTAMP not null,
	reportes int not null
);

