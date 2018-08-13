create database log DEFAULT CHARACTER SET utf8;

use log;
set names utf8;

CREATE TABLE `log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user` varchar(64) DEFAULT NULL COMMENT '用户名',
  `event` varchar(255) DEFAULT NULL COMMENT '用户操作',
  `date_time` date DEFAULT NULL COMMENT '操作时间点',
  `app` varchar(255) DEFAULT NULL COMMENT 'app',
  `city` varchar(64) DEFAULT NULL COMMENT '城市',
  `modType` varchar(255) DEFAULT NULL COMMENT 'modType',
  `ip` varchar(64) DEFAULT NULL COMMENT 'ip',
  `module` varchar(64) DEFAULT NULL COMMENT 'module',
  `userName` varchar(64) DEFAULT NULL COMMENT 'userName',
  `url` varchar(64) DEFAULT NULL COMMENT 'url',
  `modId` varchar(64) DEFAULT NULL COMMENT 'modId',
  `conditions` varchar(255) DEFAULT NULL COMMENT 'conditions',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=107 DEFAULT CHARSET=utf8;