GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
CREATE DATABASE opensips;

USE opensips;

CREATE TABLE version (
    table_name CHAR(32) NOT NULL,
    table_version INT UNSIGNED DEFAULT 0 NOT NULL,
    CONSTRAINT t_name_idx UNIQUE (table_name)
) ENGINE=InnoDB;

INSERT INTO version (table_name, table_version) values ('acc','7');

-- WARNING: Change to_tag to be DEFAULT NULL
-- because when we work in stateless mode, to_tag doen't exist !

CREATE TABLE `acc` (
`id` int(10) unsigned NOT NULL auto_increment,
`method` varchar(16) NOT NULL default '',
`from_tag` varchar(64) NOT NULL default '',
`to_tag` varchar(64) DEFAULT NULL,
`callid` varchar(128) NOT NULL default '',
`sip_code` char(3) NOT NULL default '',
`sip_reason` varchar(32) NOT NULL default '',
`time` datetime NOT NULL default CURRENT_TIMESTAMP,
`src_user` varchar(64) NOT NULL default '',
`setuptime` int(11) UNSIGNED NOT NULL DEFAULT 0,
`created` datetime DEFAULT NULL,
`duration` int(11) UNSIGNED NOT NULL DEFAULT 0,
`ms_duration` int(11) UNSIGNED NOT NULL DEFAULT 0,
`attr` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
INDEX acc_callid (`callid`),
PRIMARY KEY  (`id`)
);




