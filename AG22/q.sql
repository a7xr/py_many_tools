-- Table: ____table_prod_____q
-- -- chaine1
-- -- numvoie2
-- -- email1

DROP TABLE IF EXISTS ____table_prod_____q;

CREATE TABLE ____table_prod_____q
(
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
 

  date_cachet_poste character varying(254),
civilite character varying(254),
nom character varying(254),
prenom character varying(254),
cp character varying(254),
ville character varying(254),
adr1 character varying(254),
adr2 character varying(254),
adr3 character varying(254),
adr4 character varying(254),
pays character varying(254),
code_pays character varying(254),
email character varying(254),
mobile character varying(254),

presence_bulletin character varying(254),
j_accepte_de_recevoir character varying(254),
cnil character varying(254),
remboursement_timbre character varying(254),
presence_facture_ou_tc character varying(254),
presence_enseigne character varying(254),
saisie_code_point_de_vente character varying(254),
date_sur_ticket_de_caisse character varying(254),
presence_achat_mobile character varying(254),
presence_achat_accessoire character varying(254),
achat_simultane character varying(254),
montant_ttc_accessoire character varying(254),
montant_ht_accessoire character varying(254),
presence_code_barre_accessoire character varying(254),
original_code_barre_accessoire character varying(254),
saisie_code_barre_accessoire character varying(254),
presence_code_barre_mobile character varying(254),
saisie_code_barre_mobile character varying(254),
iban character varying(254),
bic character varying(254),
codage_canal_participation character varying(254),
mobile_d2 character varying(254),

  
  index_image text,
  doublon character varying(255),
  id_lot_numerisation integer,
  idenr integer NOT NULL DEFAULT nextval(('public.____table_prod_____q_seq'::text)::regclass),
  date_saisie date DEFAULT ('now'::text)::date,
  idexecute integer,
  nom_fichier_csv text,
  date_reception text,
  idsousdossier text,
  list_ima text,
  __s character varying(1),
  lot_operation character varying(254),
  CONSTRAINT pk_____table_prod______q PRIMARY KEY (idenr ),
  CONSTRAINT p_unique_____table_prod______q UNIQUE (n_ima , n_lot , commande , n_enr )
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ____table_prod_____q
  OWNER TO pgtantely;
GRANT ALL ON TABLE ____table_prod_____q TO pgtantely;
GRANT ALL ON TABLE ____table_prod_____q TO op;
GRANT SELECT ON TABLE ____table_prod_____q TO prep;

-- Index: idx1_____table_prod______q

DROP INDEX IF EXISTS idx1_____table_prod______q;

CREATE INDEX idx1_____table_prod______q
  ON ____table_prod_____q
  USING btree
  (commande COLLATE pg_catalog."default" , n_lot COLLATE pg_catalog."default" , __s COLLATE pg_catalog."default" );

-- Index: idx2_____table_prod______q

DROP INDEX IF EXISTS idx2_____table_prod______q;

CREATE INDEX idx2_____table_prod______q
  ON ____table_prod_____q
  USING btree
  (idexecute );

-- Index: idx3_____table_prod______q

DROP INDEX IF EXISTS idx3_____table_prod______q;

CREATE INDEX idx3_____table_prod______q
  ON ____table_prod_____q
  USING btree
  (idenr );

-- Index: idx4_____table_prod______q

DROP INDEX IF EXISTS idx4_____table_prod______q;

CREATE INDEX idx4_____table_prod______q
  ON ____table_prod_____q
  USING btree
  (n_lot COLLATE pg_catalog."default" );

-- Sequence: ____table_prod_____q_seq

DROP SEQUENCE IF EXISTS ____table_prod_____q_seq;

CREATE SEQUENCE ____table_prod_____q_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE ____table_prod_____q_seq
  OWNER TO pgtantely;
GRANT ALL ON TABLE ____table_prod_____q_seq TO pgtantely;
GRANT SELECT, UPDATE ON TABLE ____table_prod_____q_seq TO op;
GRANT SELECT ON TABLE ____table_prod_____q_seq TO prep;
