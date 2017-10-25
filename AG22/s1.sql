-- Table: ____table_prod_____s1

-- DROP TABLE ____table_prod_____s1;

CREATE TABLE ____table_prod_____s1
(
  -- reto dia tsy miova mitsn
  n_enr character varying(254),
  n_ima character varying(254),
  matricule character varying(50),
  id_commande character varying(50),
  commande character varying(50),
  etape character varying(50),
  n_lot character varying(50),
  pli character varying(50),
  lot_courrier character varying(10),
  id_web character varying(10),
  matr_operateur character varying(10),
  num_sequence character varying(9),
  n_client character varying(255),
  

  -- manomboka eto no miova
  -- miova654321654
  -- mfarana eto no miova


  -- reto dia tsy miova mitsn
  index_image text,
  doublon character varying(255),
  id_lot_numerisation integer,
  idenr integer NOT NULL DEFAULT nextval(('public.____table_prod_____s1_seq'::text)::regclass),
  date_saisie date DEFAULT ('now'::text)::date,
  idexecute integer,
  nom_fichier_csv text,
  date_reception text,
  idsousdossier text,
  list_ima text,
  __s character varying(1),
  CONSTRAINT pk_____table_prod______s1 PRIMARY KEY (idenr ),
  CONSTRAINT p_unique_____table_prod______s1 UNIQUE (n_ima , n_lot , commande , n_enr )
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ____table_prod_____s1
  OWNER TO pgtantely;
GRANT ALL ON TABLE ____table_prod_____s1 TO pgtantely;
GRANT ALL ON TABLE ____table_prod_____s1 TO op;
GRANT SELECT ON TABLE ____table_prod_____s1 TO prep;

-- Index: idx1_____table_prod______s1

-- DROP INDEX idx1_____table_prod______s1;

CREATE INDEX idx1_____table_prod______s1
  ON ____table_prod_____s1
  USING btree
  (commande COLLATE pg_catalog."default" , n_lot COLLATE pg_catalog."default" , __s COLLATE pg_catalog."default" );

-- Index: idx2_____table_prod______s1

-- DROP INDEX idx2_____table_prod______s1;

CREATE INDEX idx2_____table_prod______s1
  ON ____table_prod_____s1
  USING btree
  (idexecute );

-- Index: idx3_____table_prod______s1

-- DROP INDEX idx3_____table_prod______s1;

CREATE INDEX idx3_____table_prod______s1
  ON ____table_prod_____s1
  USING btree
  (idenr );

-- Index: idx4_____table_prod______s1

-- DROP INDEX idx4_____table_prod______s1;

CREATE INDEX idx4_____table_prod______s1
  ON ____table_prod_____s1
  USING btree
  (n_lot COLLATE pg_catalog."default" );

-- Sequence: ____table_prod_____s1_seq

-- DROP SEQUENCE ____table_prod_____s1_seq;

CREATE SEQUENCE ____table_prod_____s1_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE ____table_prod_____s1_seq
  OWNER TO pgtantely;
GRANT ALL ON TABLE ____table_prod_____s1_seq TO pgtantely;
GRANT SELECT, UPDATE ON TABLE ____table_prod_____s1_seq TO op;
GRANT SELECT ON TABLE ____table_prod_____s1_seq TO prep;
