drop database proyecto_flask;
create database proyecto_flask;
use proyecto_flask;

create table programador(
	id int(255) auto_increment primary key,
    lenguaje varchar(255),
    annos_experiencia int(45),
    sueldo decimal (19.4),
    ciudad varchar(255)
);

insert into programador (lenguaje,annos_experiencia,sueldo,ciudad) values ('Python',2,600000,'San Antonio');

select * from programador;