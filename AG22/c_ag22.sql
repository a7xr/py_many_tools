-- Table: sgal97_c

-- DROP TABLE sgal97_c;

CREATE TABLE sgal97_c
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
 

   -- manomboka eto no miova
  date_cachet_poste character varying(254),
  civilite character varying(254),
  nom character varying(254),
  prenom character varying(254),
  cp character varying(254),
  ville character varying(254),
  numvoie character varying(254),
  chaine1 character varying(254),
  adr1 character varying(254),
  numvoie2 character varying(254),
  chaine2 character varying(254),
  adr2 character varying(254),
  numvoie3 character varying(254),
  chaine3 character varying(254),
  adr3 character varying(254),
  adr4 character varying(254),
  pays character varying(254),
  email1 character varying(254),
  email2 character varying(254),
  mobile character varying(254),
  iban character varying(254),
  bic character varying(254),
  j_accepte_recevoir_info_commerciale character varying(254),
  presence_bulletin character varying(254),
  cnil character varying(254),
  presence_facture_ou_tc character varying(254),
  presence_enseigne_fnac character varying(254),
  presence_achat_mobile character varying(254),
  date_sur_facture character varying(254),
  montant_ttc_mobile character varying(254),
  montant_ht_mobile character varying(254),
  souscription_forfait_sensation character varying(254),
  changement_de_mobile character varying(254),
  presence_contrat_service character varying(254),
  presence_forfait_sensation character varying(254),
  presence_derniere_facture character varying(254),
  presence_avenant_contrat character varying(254),
  presence_premiere_facture character varying(254),
  date_facture_superieure character varying(254),
  codage_forfait_sensation character varying(254),
  codage_forfait_bbox character varying(254),
  mobile_d2 character varying(254),
  montant_ttc_mobile_d2 character varying(254),
  montant_ht_mobile_d2 character varying(254),
  -- mfarana eto no miova

 
  index_image text,
  doublon character varying(255),
  id_lot_numerisation integer,
  idenr integer NOT NULL DEFAULT nextval(('public.sgal97_c_seq'::text)::regclass),
  date_saisie date DEFAULT ('now'::text)::date,
  idexecute integer,
  nom_fichier_csv text,
  date_reception text,
  idsousdossier text,
  list_ima text,
  __s character varying(1),
  CONSTRAINT pk_sgal97__c PRIMARY KEY (idenr ),
  CONSTRAINT p_unique_sgal97__c UNIQUE (n_ima , n_lot , commande , n_enr )
)
WITH (
  OIDS=TRUE
);
ALTER TABLE sgal97_c
  OWNER TO pgtantely;
GRANT ALL ON TABLE sgal97_c TO pgtantely;
GRANT ALL ON TABLE sgal97_c TO op;
GRANT SELECT ON TABLE sgal97_c TO prep;

-- Index: idx1_sgal97__c

-- DROP INDEX idx1_sgal97__c;

CREATE INDEX idx1_sgal97__c
  ON sgal97_c
  USING btree
  (commande COLLATE pg_catalog."default" , n_lot COLLATE pg_catalog."default" , __s COLLATE pg_catalog."default" );

-- Index: idx2_sgal97__c

-- DROP INDEX idx2_sgal97__c;

CREATE INDEX idx2_sgal97__c
  ON sgal97_c
  USING btree
  (idexecute );

-- Index: idx3_sgal97__c

-- DROP INDEX idx3_sgal97__c;

CREATE INDEX idx3_sgal97__c
  ON sgal97_c
  USING btree
  (idenr );

-- Index: idx4_sgal97__c

-- DROP INDEX idx4_sgal97__c;

CREATE INDEX idx4_sgal97__c
  ON sgal97_c
  USING btree
  (n_lot COLLATE pg_catalog."default" );

-- Sequence: sgal97_c_seq

-- DROP SEQUENCE sgal97_c_seq;

CREATE SEQUENCE sgal97_c_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE sgal97_c_seq
  OWNER TO pgtantely;
GRANT ALL ON TABLE sgal97_c_seq TO pgtantely;
GRANT SELECT, UPDATE ON TABLE sgal97_c_seq TO op;
GRANT SELECT ON TABLE sgal97_c_seq TO prep;
