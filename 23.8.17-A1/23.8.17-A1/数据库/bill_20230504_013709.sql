-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: bill
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `data`
--

DROP TABLE IF EXISTS `data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data` (
  `group_id` bigint NOT NULL,
  `amount` float DEFAULT NULL,
  `timestamp` bigint DEFAULT NULL,
  `rate` float DEFAULT NULL,
  `usd_rate` float DEFAULT NULL,
  `respondent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `operator` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data`
--

LOCK TABLES `data` WRITE;
/*!40000 ALTER TABLE `data` DISABLE KEYS */;
INSERT INTO `data` VALUES (-1001932434598,1,1683021754,0,8,'','Aaq99854','add'),(-1001932434598,2,1683021757,0,8,'','Aaq99854','add'),(-1001932434598,3,1683021760,0,8,'','Aaq99854','add'),(-1001932434598,5,1683021763,0,8,'','Aaq99854','add'),(-1001932434598,8,1683021769,0,8,'','Aaq99854','add'),(-1001932434598,10,1683021776,0,8,'','Aaq99854','add'),(-1001932434598,50,1683021779,0,8,'','Aaq99854','add'),(-1001932434598,200,1683021822,0,8,'','Aaq99854','add'),(-1001932434598,50,1683021829,0,8,'','Aaq99854','add'),(-1001932434598,100,1683022432,0,8,'','Aaq99854','add'),(-1001932434598,0,1683023305,0,8,'','Aaq99854','add'),(-1001515044657,5,1683023518,0,8,'','王大锤','add'),(-1001836046135,100,1683084822,0.05,0,'','sychoc','add'),(-1001836046135,300,1683084824,0.05,0,'','sychoc','add'),(-1001836046135,555,1683084826,0.05,0,'','sychoc','add'),(-1001836046135,555,1683084846,0.05,0,'','sychoc','add'),(-1001836046135,333,1683084848,0.05,0,'','sychoc','add'),(-1001836046135,500,1683084935,0.05,6.8,'','sychoc','add'),(-1001256521791,154,1683113917,0,0,'','王大锤','add'),(-1001256521791,50,1683124095,0,0,'','王大锤','add'),(-1001256521791,10,1683124109,0,8,'','王大锤','add'),(-1001256521791,9,1683124127,0,8,'','王大锤','add'),(-1001256521791,10,1683124428,0,8,'','王大锤','add'),(-1001256521791,12,1683124430,0,8,'','王大锤','add'),(-1001256521791,23,1683124433,0,8,'','王大锤','add'),(-1001256521791,1,1683124502,0,8,'','王大锤','add'),(-1001256521791,1,1683124504,0,8,'','王大锤','add'),(-1001256521791,2,1683124508,0,8,'','王大锤','add'),(-1001256521791,5,1683124611,0,8,'','王大锤','add'),(-1001256521791,12,1683124618,0,8,'','王大锤','add'),(-1001256521791,52,1683124621,0,8,'','王大锤','add');
/*!40000 ALTER TABLE `data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data2`
--

DROP TABLE IF EXISTS `data2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data2` (
  `group_id` bigint DEFAULT NULL,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `rmb` float DEFAULT NULL,
  `usdt` float DEFAULT NULL,
  `timestamp` bigint DEFAULT NULL,
  `respondent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `operator` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `type` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data2`
--

LOCK TABLES `data2` WRITE;
/*!40000 ALTER TABLE `data2` DISABLE KEYS */;
INSERT INTO `data2` VALUES (-1001932434598,'30U',240,30,1683022390,'','Aaq99854','out');
/*!40000 ALTER TABLE `data2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groups` (
  `group_id` bigint NOT NULL,
  `owner` bigint DEFAULT NULL,
  `operator` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `rate` float DEFAULT NULL,
  `usd_rate` float DEFAULT NULL,
  `state` tinyint DEFAULT NULL,
  `display` int DEFAULT NULL,
  `operator_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `u_display` tinyint DEFAULT NULL,
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `ad_display` tinyint DEFAULT NULL,
  `ad` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `rule` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `welcome` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `authorizer` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `authorizer_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `gear` float DEFAULT NULL COMMENT 'usdt 挡位',
  `adjust` float DEFAULT NULL COMMENT 'usdt 微调',
  `mrate` float DEFAULT NULL COMMENT 'usdt 费率',
  `kefu` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `warn_rmb` float DEFAULT NULL,
  `warn_u` float DEFAULT NULL,
  `overs` tinyint DEFAULT NULL,
  `uuu` float DEFAULT NULL COMMENT 'USDT 固定费率',
  PRIMARY KEY (`group_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES (-1001836046135,5732433547,'5732433547,',0.05,6.8,1,1,'T,',1,'0',1,'0','0','用户名称：{name}\n用户名：{username}\n用户ID：{id}\n欢迎加入此群！','5732433547','A,',1,0,0,'0',0,0,0,0),(-1001256521791,5355607184,'5355607184,',0,8,1,1,'T,',1,'0',1,'0','0','用户名称：{name}\n用户名：{username}\n用户ID：{id}\n欢迎加入此群！','5355607184','A,',1,0,0,'0',0,0,0,0),(-803587780,5348262286,'5348262286,',-1,0,0,1,'T,',1,'0',1,'0','0','用户名称：{name}\n用户名：{username}\n用户ID：{id}\n欢迎加入此群！','5348262286','A,',1,0,0,'0',0,0,0,0);
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` bigint NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `username` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `authorized` bigint DEFAULT NULL,
  `free` tinyint DEFAULT NULL,
  `shouquan` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `shouquan_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `liangtian` tinyint DEFAULT NULL,
  `daoqi` tinyint DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (5323355513,'维多利亚','wise776',1683110686,0,'5323355513,','admin,',1,1),(5348262286,'建群号','SVIP9915',1683107686,0,'5348262286,1530462768,1569681506,6075246671,5323355513,5965224227,','admin,@BillMonta,@Valter_saragoca,@Aaq99854,@wise776,@xuezhang,',1,1),(5355607184,'王大锤',' ',1683135501,0,'5355607184,','admin,',1,1),(5732433547,'SychO','sychoc',1683106253,0,'5732433547,5307210553,5323355513,5714430802,5925982453,6202091685,','admin,@excel003,@wise776,@otrxbot,@trx2222_bot,@qun666bot,',1,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'bill'
--

--
-- Dumping routines for database 'bill'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-04  1:37:09
