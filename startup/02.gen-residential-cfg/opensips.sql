
CREATE DATABASE opensips;

USE opensips;

CREATE TABLE version (
    table_name CHAR(32) NOT NULL,
    table_version INT UNSIGNED DEFAULT 0 NOT NULL,
    CONSTRAINT t_name_idx UNIQUE (table_name)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('location','1013');
CREATE TABLE location (
    contact_id BIGINT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username CHAR(64) DEFAULT '' NOT NULL,
    domain CHAR(64) DEFAULT NULL,
    contact TEXT NOT NULL,
    received CHAR(255) DEFAULT NULL,
    path CHAR(255) DEFAULT NULL,
    expires INT(10) UNSIGNED NOT NULL,
    q FLOAT(10,2) DEFAULT 1.0 NOT NULL,
    callid CHAR(255) DEFAULT 'Default-Call-ID' NOT NULL,
    cseq INT(11) DEFAULT 13 NOT NULL,
    last_modified DATETIME DEFAULT '1900-01-01 00:00:01' NOT NULL,
    flags INT(11) DEFAULT 0 NOT NULL,
    cflags CHAR(255) DEFAULT NULL,
    user_agent CHAR(255) DEFAULT '' NOT NULL,
    socket CHAR(64) DEFAULT NULL,
    methods INT(11) DEFAULT NULL,
    sip_instance CHAR(255) DEFAULT NULL,
    kv_store TEXT(512) DEFAULT NULL,
    attr CHAR(255) DEFAULT NULL
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('acc','7');
CREATE TABLE acc (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    method CHAR(16) DEFAULT '' NOT NULL,
    from_tag CHAR(64) DEFAULT '' NOT NULL,
    to_tag CHAR(64) DEFAULT '' NOT NULL,
    callid CHAR(64) DEFAULT '' NOT NULL,
    sip_code CHAR(3) DEFAULT '' NOT NULL,
    sip_reason CHAR(32) DEFAULT '' NOT NULL,
    time DATETIME NOT NULL,
    duration INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    ms_duration INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    setuptime INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    created DATETIME DEFAULT NULL
) ENGINE=InnoDB;

CREATE INDEX callid_idx ON acc (callid);

INSERT INTO version (table_name, table_version) values ('missed_calls','5');
CREATE TABLE missed_calls (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    method CHAR(16) DEFAULT '' NOT NULL,
    from_tag CHAR(64) DEFAULT '' NOT NULL,
    to_tag CHAR(64) DEFAULT '' NOT NULL,
    callid CHAR(64) DEFAULT '' NOT NULL,
    sip_code CHAR(3) DEFAULT '' NOT NULL,
    sip_reason CHAR(32) DEFAULT '' NOT NULL,
    time DATETIME NOT NULL,
    setuptime INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    created DATETIME DEFAULT NULL
) ENGINE=InnoDB;

CREATE INDEX callid_idx ON missed_calls (callid);

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

INSERT INTO version (table_name, table_version) values ('dbaliases','2');
CREATE TABLE dbaliases (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    alias_username CHAR(64) DEFAULT '' NOT NULL,
    alias_domain CHAR(64) DEFAULT '' NOT NULL,
    username CHAR(64) DEFAULT '' NOT NULL,
    domain CHAR(64) DEFAULT '' NOT NULL,
    CONSTRAINT alias_idx UNIQUE (alias_username, alias_domain)
) ENGINE=InnoDB;

CREATE INDEX target_idx ON dbaliases (username, domain);

INSERT INTO version (table_name, table_version) values ('presentity','5');
CREATE TABLE presentity (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username CHAR(64) NOT NULL,
    domain CHAR(64) NOT NULL,
    event CHAR(64) NOT NULL,
    etag CHAR(64) NOT NULL,
    expires INT(11) NOT NULL,
    received_time INT(11) NOT NULL,
    body BLOB DEFAULT NULL,
    extra_hdrs BLOB DEFAULT NULL,
    sender CHAR(255) DEFAULT NULL,
    CONSTRAINT presentity_idx UNIQUE (username, domain, event, etag)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('active_watchers','12');
CREATE TABLE active_watchers (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    presentity_uri CHAR(255) NOT NULL,
    watcher_username CHAR(64) NOT NULL,
    watcher_domain CHAR(64) NOT NULL,
    to_user CHAR(64) NOT NULL,
    to_domain CHAR(64) NOT NULL,
    event CHAR(64) DEFAULT 'presence' NOT NULL,
    event_id CHAR(64),
    to_tag CHAR(64) NOT NULL,
    from_tag CHAR(64) NOT NULL,
    callid CHAR(64) NOT NULL,
    local_cseq INT(11) NOT NULL,
    remote_cseq INT(11) NOT NULL,
    contact CHAR(255) NOT NULL,
    record_route TEXT,
    expires INT(11) NOT NULL,
    status INT(11) DEFAULT 2 NOT NULL,
    reason CHAR(64),
    version INT(11) DEFAULT 0 NOT NULL,
    socket_info CHAR(64) NOT NULL,
    local_contact CHAR(255) NOT NULL,
    sharing_tag CHAR(32) DEFAULT NULL,
    CONSTRAINT active_watchers_idx UNIQUE (presentity_uri, callid, to_tag, from_tag)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('watchers','4');
CREATE TABLE watchers (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    presentity_uri CHAR(255) NOT NULL,
    watcher_username CHAR(64) NOT NULL,
    watcher_domain CHAR(64) NOT NULL,
    event CHAR(64) DEFAULT 'presence' NOT NULL,
    status INT(11) NOT NULL,
    reason CHAR(64),
    inserted_time INT(11) NOT NULL,
    CONSTRAINT watcher_idx UNIQUE (presentity_uri, watcher_username, watcher_domain, event)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('xcap','4');
CREATE TABLE xcap (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username CHAR(64) NOT NULL,
    domain CHAR(64) NOT NULL,
    doc LONGBLOB NOT NULL,
    doc_type INT(11) NOT NULL,
    etag CHAR(64) NOT NULL,
    source INT(11) NOT NULL,
    doc_uri CHAR(255) NOT NULL,
    port INT(11) NOT NULL,
    CONSTRAINT account_doc_type_idx UNIQUE (username, domain, doc_type, doc_uri)
) ENGINE=InnoDB;

CREATE INDEX source_idx ON xcap (source);

INSERT INTO version (table_name, table_version) values ('pua','9');
CREATE TABLE pua (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    pres_uri CHAR(255) NOT NULL,
    pres_id CHAR(255) NOT NULL,
    event INT(11) NOT NULL,
    expires INT(11) NOT NULL,
    desired_expires INT(11) NOT NULL,
    flag INT(11) NOT NULL,
    etag CHAR(64),
    tuple_id CHAR(64),
    watcher_uri CHAR(255),
    to_uri CHAR(255),
    call_id CHAR(64),
    to_tag CHAR(64),
    from_tag CHAR(64),
    cseq INT(11),
    record_route TEXT,
    contact CHAR(255),
    remote_contact CHAR(255),
    version INT(11),
    extra_headers TEXT,
    sharing_tag CHAR(32) DEFAULT NULL
) ENGINE=InnoDB;

CREATE INDEX del1_idx ON pua (pres_uri, event);
CREATE INDEX del2_idx ON pua (expires);
CREATE INDEX update_idx ON pua (pres_uri, pres_id, flag, event);

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

INSERT INTO version (table_name, table_version) values ('dialplan','5');
CREATE TABLE dialplan (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    dpid INT(11) NOT NULL,
    pr INT(11) DEFAULT 0 NOT NULL,
    match_op INT(11) NOT NULL,
    match_exp CHAR(64) NOT NULL,
    match_flags INT(11) DEFAULT 0 NOT NULL,
    subst_exp CHAR(64) DEFAULT NULL,
    repl_exp CHAR(32) DEFAULT NULL,
    timerec CHAR(255) DEFAULT NULL,
    disabled INT(11) DEFAULT 0 NOT NULL,
    attrs CHAR(255) DEFAULT NULL
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('dr_gateways','6');
CREATE TABLE dr_gateways (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    gwid CHAR(64) NOT NULL,
    type INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    address CHAR(128) NOT NULL,
    strip INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    pri_prefix CHAR(16) DEFAULT NULL,
    attrs CHAR(255) DEFAULT NULL,
    probe_mode INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    state INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    socket CHAR(128) DEFAULT NULL,
    description CHAR(128) DEFAULT NULL,
    CONSTRAINT dr_gw_idx UNIQUE (gwid)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('dr_rules','4');
CREATE TABLE dr_rules (
    ruleid INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    groupid CHAR(255) NOT NULL,
    prefix CHAR(64) NOT NULL,
    timerec CHAR(255) DEFAULT NULL,
    priority INT(11) DEFAULT 0 NOT NULL,
    routeid CHAR(255) DEFAULT NULL,
    gwlist CHAR(255),
    sort_alg CHAR(1) DEFAULT 'N' NOT NULL,
    sort_profile INT(10) UNSIGNED DEFAULT NULL,
    attrs CHAR(255) DEFAULT NULL,
    description CHAR(128) DEFAULT NULL
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('dr_carriers','3');
CREATE TABLE dr_carriers (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    carrierid CHAR(64) NOT NULL,
    gwlist CHAR(255) NOT NULL,
    flags INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    sort_alg CHAR(1) DEFAULT 'N' NOT NULL,
    state INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    attrs CHAR(255) DEFAULT NULL,
    description CHAR(128) DEFAULT NULL,
    CONSTRAINT dr_carrier_idx UNIQUE (carrierid)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('dr_groups','2');
CREATE TABLE dr_groups (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username CHAR(64) NOT NULL,
    domain CHAR(128) DEFAULT NULL,
    groupid INT(11) UNSIGNED DEFAULT 0 NOT NULL,
    description CHAR(128) DEFAULT NULL
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('dr_partitions','1');
CREATE TABLE dr_partitions (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    partition_name CHAR(255) NOT NULL,
    db_url CHAR(255) NOT NULL,
    drd_table CHAR(255),
    drr_table CHAR(255),
    drg_table CHAR(255),
    drc_table CHAR(255),
    ruri_avp CHAR(255),
    gw_id_avp CHAR(255),
    gw_priprefix_avp CHAR(255),
    gw_sock_avp CHAR(255),
    rule_id_avp CHAR(255),
    rule_prefix_avp CHAR(255),
    carrier_id_avp CHAR(255)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('domain','3');
CREATE TABLE domain (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    domain CHAR(64) DEFAULT '' NOT NULL,
    attrs CHAR(255) DEFAULT NULL,
    last_modified DATETIME DEFAULT '1900-01-01 00:00:01' NOT NULL,
    CONSTRAINT domain_idx UNIQUE (domain)
) ENGINE=InnoDB;
