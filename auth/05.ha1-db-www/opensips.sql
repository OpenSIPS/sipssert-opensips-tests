
CREATE DATABASE opensips;

USE opensips;

CREATE TABLE version (
    table_name CHAR(32) NOT NULL,
    table_version INT UNSIGNED DEFAULT 0 NOT NULL,
    CONSTRAINT t_name_idx UNIQUE (table_name)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('subscriber','8');
CREATE TABLE subscriber (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username CHAR(64) DEFAULT '' NOT NULL,
    domain CHAR(64) DEFAULT '' NOT NULL,
    password CHAR(25) DEFAULT '' NOT NULL,
    email_address CHAR(64) DEFAULT '' NOT NULL,
    ha1 CHAR(64) DEFAULT '' NOT NULL,
    ha1_sha256 CHAR(64) DEFAULT '' NOT NULL,
    ha1_sha512t256 CHAR(64) DEFAULT '' NOT NULL,
    rpid CHAR(64) DEFAULT NULL,
    CONSTRAINT account_idx UNIQUE (username, domain)
) ENGINE=InnoDB;

CREATE INDEX username_idx ON subscriber (username);

INSERT INTO version (table_name, table_version) values ('uri','2');
CREATE TABLE uri (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username CHAR(64) DEFAULT '' NOT NULL,
    domain CHAR(64) DEFAULT '' NOT NULL,
    uri_user CHAR(64) DEFAULT '' NOT NULL,
    last_modified DATETIME DEFAULT '1900-01-01 00:00:01' NOT NULL,
    CONSTRAINT account_idx UNIQUE (username, domain, uri_user)
) ENGINE=InnoDB;

INSERT INTO `subscriber` VALUES (1,'testing','','','',MD5('testing:192.168.52.1:T3st|n6'),'','',NULL);
