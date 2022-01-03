--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: espacio_reporte; Type: TYPE; Schema: public; Owner: dengue_bot
--

CREATE TYPE public.espacio_reporte AS ENUM (
    '¡Sí pude eliminarlo!', 
    'Predio deshabilitado o sin acceso',
    'No se encuentra lx residente presente',
    'Lx residente no accedió a realizar la acción', 
    'El gran volumen requiere asistencia'
);


ALTER TYPE public.espacio_reporte OWNER TO dengue_bot;

--
-- Name: tipo_reporte; Type: TYPE; Schema: public; Owner: dengue_bot
--

CREATE TYPE public.tipo_reporte AS ENUM (
    'Basural a cielo abierto',
    'Acumulación de basura en la calle',
    'Neumáticos en desuso',
    'Chatarra, chapas u otros objetos voluminosos al descubierto',
    'Recipiente', 
    'Terreno sin desmalezar',
    'Vivienda con objetos que acumulan agua'
);


ALTER TYPE public.tipo_reporte OWNER TO dengue_bot;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: agente; Type: TABLE; Schema: public; Owner: dengue_bot
--

CREATE TABLE public.agente (
    agente_id integer NOT NULL,
    nombre character varying(64) NOT NULL,
    apellido character varying(64) NULL,
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    fecha timestamp without time zone NOT NULL,
    reportes integer NOT NULL
);


ALTER TABLE public.agente OWNER TO dengue_bot;

--
-- Name: magnitud_reporte; Type: TYPE; Schema: public; Owner: dengue_bot
--

CREATE TYPE public.magnitud_reporte AS ENUM (
    'nan' 
);


ALTER TYPE public.magnitud_reporte OWNER TO dengue_bot;

--
-- Name: reporte; Type: TABLE; Schema: public; Owner: dengue_bot
--

CREATE TABLE public.reporte (
    agente_id integer NOT NULL,
    numero integer NOT NULL,
    tipo public.tipo_reporte NOT NULL,
    magnitud public.magnitud_reporte NOT NULL,
    espacio public.espacio_reporte NOT NULL,
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    inicio timestamp without time zone NOT NULL,
    final timestamp without time zone NOT NULL
);


ALTER TABLE public.reporte OWNER TO dengue_bot;

--
-- Data for Name: agente; Type: TABLE DATA; Schema: public; Owner: dengue_bot
--

COPY public.agente (agente_id, nombre, apellido, latitud, longitud, fecha, reportes) FROM stdin;
657804218	Gustavo	Landfried	4	-73	2019-12-23 20:55:05	0
\.


--
-- Data for Name: reporte; Type: TABLE DATA; Schema: public; Owner: dengue_bot
--

COPY public.reporte (agente_id, numero, tipo, magnitud, espacio, latitud, longitud, inicio, final) FROM stdin;
\.


--
-- Name: agente agente_pkey; Type: CONSTRAINT; Schema: public; Owner: dengue_bot
--

ALTER TABLE ONLY public.agente
    ADD CONSTRAINT agente_pkey PRIMARY KEY (agente_id);


--
-- Name: reporte reporte_pkey; Type: CONSTRAINT; Schema: public; Owner: dengue_bot
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_pkey PRIMARY KEY (agente_id, numero);


--
-- Name: reporte reporte_agente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dengue_bot
--

ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_agente_id_fkey FOREIGN KEY (agente_id) REFERENCES public.agente(agente_id);


--
-- PostgreSQL database dump complete
