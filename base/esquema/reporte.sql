create type tipo_reporte as enum ('Basural a cielo abierto',
    'Acumulación de basura en la calle',
    'Neumáticos en desuso',
    'Chatarra, chapas u otros objetos voluminosos al descubierto',
    'Recipiente', 
    'Terreno sin desmalezar',
    'Vivienda con objetos que acumulan agua');
create type magnitud_reporte as enum ('nan');
create type espacio_reporte as enum ('¡Sí pude eliminarlo!', 
    'Predio deshabilitado o sin acceso',
    'No se encuentra lx residente presente',
    'Lx residente no accedió a realizar la acción', 
    'El gran volumen requiere asistencia');

create table reporte (
	agente_id int not null,
	numero int not null,
	tipo tipo_reporte not null,
	magnitud magnitud_reporte not null,
	espacio espacio_reporte not null,
	latitud float not null,
	longitud float not null,
	inicio TIMESTAMP not null,
	final TIMESTAMP not null,
	 primary key(agente_id , numero),
	foreign key (agente_id)  references agente (agente_id)
);

