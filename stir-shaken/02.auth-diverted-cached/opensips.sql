
CREATE DATABASE opensips;

USE opensips;

CREATE TABLE version (
    table_name CHAR(32) NOT NULL,
    table_version INT UNSIGNED DEFAULT 0 NOT NULL,
    CONSTRAINT t_name_idx UNIQUE (table_name)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('dialog','12');
CREATE TABLE dialog (
    dlg_id BIGINT(10) UNSIGNED PRIMARY KEY NOT NULL,
    callid CHAR(255) NOT NULL,
    from_uri CHAR(255) NOT NULL,
    from_tag CHAR(64) NOT NULL,
    to_uri CHAR(255) NOT NULL,
    to_tag CHAR(64) NOT NULL,
    mangled_from_uri CHAR(64) DEFAULT NULL,
    mangled_to_uri CHAR(64) DEFAULT NULL,
    caller_cseq CHAR(11) NOT NULL,
    callee_cseq CHAR(11) NOT NULL,
    caller_ping_cseq INT(11) UNSIGNED NOT NULL,
    callee_ping_cseq INT(11) UNSIGNED NOT NULL,
    caller_route_set TEXT(512),
    callee_route_set TEXT(512),
    caller_contact CHAR(255),
    callee_contact CHAR(255),
    caller_sock CHAR(64) NOT NULL,
    callee_sock CHAR(64) NOT NULL,
    state INT(10) UNSIGNED NOT NULL,
    start_time INT(10) UNSIGNED NOT NULL,
    timeout INT(10) UNSIGNED NOT NULL,
    vars BLOB(4096) DEFAULT NULL,
    profiles TEXT(512) DEFAULT NULL,
    script_flags CHAR(255) DEFAULT NULL,
    module_flags INT(10) UNSIGNED DEFAULT 0 NOT NULL,
    flags INT(10) UNSIGNED DEFAULT 0 NOT NULL,
    rt_on_answer CHAR(64) DEFAULT NULL,
    rt_on_timeout CHAR(64) DEFAULT NULL,
    rt_on_hangup CHAR(64) DEFAULT NULL
) ENGINE=InnoDB;


CREATE TABLE `man_certificates_cache` (
  `id` int(11) NOT NULL,
  `x5u` varchar(255) NOT NULL,
  `certificate` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `man_certificates_cache`
  ADD PRIMARY KEY (`id`),
  ADD KEY `x5u` (`x5u`);

ALTER TABLE `man_certificates_cache`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

INSERT INTO `man_certificates_cache` (`id`, `x5u`, `certificate`) VALUES
(1, 'https://certs.example.org/public_am.pem', '-----BEGIN CERTIFICATE-----\r\nMIICCjCCAbGgAwIBAgIUSNIbrqdPoECfW3i6BBGPlchSkHMwCgYIKoZIzj0EAwIw\r\nRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoMGElu\r\ndGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yNTExMjgwOTE1NDZaFw0yODAzMDIw\r\nOTE1NDZaMGoxCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJWQTESMBAGA1UEBwwJU29t\r\nZXdoZXJlMRowGAYDVQQKDBFBY21lVGVsZWNvbSwgSW5jLjENMAsGA1UECwwEVk9J\r\nUDEPMA0GA1UEAwwGU0hBS0VOMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEaPyS\r\nscAtke1Xu+F3WiCCZVJu9fENVSFyUsk9qcdAn53KeCz3DJgrtXRpuL8BWHIZPnzm\r\niD50oC0bIehHBC1PzKNaMFgwFgYIKwYBBQUHARoECjAIoAYWBDEwMDEwHQYDVR0O\r\nBBYEFNJmDpreW3vtHMtze5+6yK6bw0CYMB8GA1UdIwQYMBaAFLWmK4xYG5/pKSUM\r\nPUnNcNYMVfSUMAoGCCqGSM49BAMCA0cAMEQCIAeFEP+kDmQMYa0YWYqQ5o5CEnNB\r\nSRaIcwQbJ74ZDzmFAiBMfLouPmcRroJJFOmFweHxDcsdnzTCSpmX2alU3gCDWw==\r\n-----END CERTIFICATE-----\n');

