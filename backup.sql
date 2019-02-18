-- MySQL dump 10.13  Distrib 5.5.54, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: agrowsoftdb
-- ------------------------------------------------------
-- Server version	5.5.54-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `conditions`
--

DROP TABLE IF EXISTS `conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conditions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Greenhouse` varchar(45) NOT NULL DEFAULT '',
  `Date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `Time` time NOT NULL DEFAULT '00:00:00',
  `Temperature` float NOT NULL DEFAULT '0',
  `Humidity` float NOT NULL DEFAULT '0',
  `Light` float NOT NULL DEFAULT '0',
  `Moles` float NOT NULL DEFAULT '0',
  `Serialnum` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=11002 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conditions`
--

LOCK TABLES `conditions` WRITE;
/*!40000 ALTER TABLE `conditions` DISABLE KEYS */;
/*!40000 ALTER TABLE `conditions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conditionstemp`
--

DROP TABLE IF EXISTS `conditionstemp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conditionstemp` (
  `ID` int(11) NOT NULL DEFAULT '0',
  `Greenhouse` varchar(45) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `Date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `Time` time NOT NULL DEFAULT '00:00:00',
  `Temperature` float NOT NULL DEFAULT '0',
  `Humidity` float NOT NULL DEFAULT '0',
  `Light` float NOT NULL DEFAULT '0',
  `Moles` float NOT NULL DEFAULT '0',
  `Serialnum` bigint(20) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conditionstemp`
--

LOCK TABLES `conditionstemp` WRITE;
/*!40000 ALTER TABLE `conditionstemp` DISABLE KEYS */;
INSERT INTO `conditionstemp` VALUES (0,'Cucumber','2015-01-17 00:00:00','11:45:53',66.8988,13.2528,406,0.0371388,712110088);
/*!40000 ALTER TABLE `conditionstemp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controllers`
--

DROP TABLE IF EXISTS `controllers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controllers` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `customerID` bigint(20) NOT NULL,
  `Serialnum` bigint(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controllers`
--

LOCK TABLES `controllers` WRITE;
/*!40000 ALTER TABLE `controllers` DISABLE KEYS */;
INSERT INTO `controllers` VALUES (16,1,712110135);
/*!40000 ALTER TABLE `controllers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controls`
--

DROP TABLE IF EXISTS `controls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controls` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `Greenhouse` varchar(25) NOT NULL,
  `Serialnum` bigint(20) NOT NULL,
  `Control` varchar(45) NOT NULL,
  `State` int(11) NOT NULL,
  `Date` datetime NOT NULL,
  `Time` time NOT NULL,
  `dateandtime` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=30297 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controls`
--

LOCK TABLES `controls` WRITE;
/*!40000 ALTER TABLE `controls` DISABLE KEYS */;
/*!40000 ALTER TABLE `controls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controlstemp`
--

DROP TABLE IF EXISTS `controlstemp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controlstemp` (
  `ID` bigint(20) NOT NULL DEFAULT '0',
  `Greenhouse` varchar(25) CHARACTER SET utf8 NOT NULL,
  `Serialnum` bigint(20) NOT NULL,
  `Control` varchar(45) CHARACTER SET utf8 NOT NULL,
  `State` int(11) NOT NULL,
  `Date` datetime NOT NULL,
  `Time` time NOT NULL,
  `dateandtime` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controlstemp`
--

LOCK TABLES `controlstemp` WRITE;
/*!40000 ALTER TABLE `controlstemp` DISABLE KEYS */;
INSERT INTO `controlstemp` VALUES (0,'Tomato',712110019,'Heater1',0,'2014-10-01 00:00:00','16:26:17','2014-10-01 16:26:17'),(0,'Tomato',712110019,'Heater2',0,'2014-10-01 00:00:00','16:26:58','2014-10-01 16:26:58'),(0,'Tomato',712110019,'Cooling1',0,'2014-10-04 00:00:00','21:35:17','2014-10-04 21:35:17'),(0,'Tomato',712110019,'Cooling2',0,'2014-10-04 00:00:00','21:35:17','2014-10-04 21:35:17'),(0,'Tomato',712110019,'Cooling3',0,'2014-10-01 00:00:00','16:29:17','2014-10-01 16:29:17'),(0,'Tomato',712110019,'Cooling4',0,'2014-10-01 00:00:00','16:32:34','2014-10-01 16:32:34'),(0,'Tomato',712110019,'Dehumidify',0,'2014-10-04 00:00:00','21:35:17','2014-10-04 21:35:17'),(0,'Tomato',712110019,'IPM',0,'1999-12-31 00:00:00','19:05:08','1999-12-31 19:05:08'),(0,'Tomato',712110019,'Zone1',0,'2014-10-01 00:00:00','16:08:10','2014-10-01 16:08:10'),(0,'Tomato',712110019,'Zone2',0,'2014-10-01 00:00:00','16:08:20','2014-10-01 16:08:20'),(0,'Tomato',712110019,'Zone3',0,'2014-10-01 00:00:00','16:08:30','2014-10-01 16:08:30'),(0,'Tomato',712110019,'Zone4',0,'2014-10-01 00:00:00','16:08:40','2014-10-01 16:08:40'),(0,'Tomato',712110019,'Zone5',0,'2014-10-01 00:00:00','16:08:51','2014-10-01 16:08:51'),(0,'Tomato',712110019,'Zone6',0,'1999-12-31 00:00:00','19:05:08','1999-12-31 19:05:08'),(0,'Tomato',712110019,'Zone7',0,'1999-12-31 00:00:00','19:05:08','1999-12-31 19:05:08'),(0,'Tomato',712110019,'Zone8',0,'1999-12-31 00:00:00','19:05:08','1999-12-31 19:05:08'),(0,'Tomato',712110019,'Zone9',0,'1999-12-31 00:00:00','19:05:08','1999-12-31 19:05:08'),(0,'Tomato',712110019,'Zone10',0,'1999-12-31 00:00:00','19:05:08','1999-12-31 19:05:08'),(0,'Tomato',712110019,'Alarm',0,'2014-10-01 00:00:00','16:25:21','2014-10-01 16:25:21');
/*!40000 ALTER TABLE `controlstemp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL DEFAULT '',
  `first_name` varchar(255) NOT NULL DEFAULT '',
  `last_name` varchar(255) NOT NULL DEFAULT '',
  `mail_address` varchar(255) NOT NULL DEFAULT '',
  `city` varchar(255) NOT NULL DEFAULT '',
  `state` varchar(255) NOT NULL DEFAULT '',
  `zip` int(11) NOT NULL DEFAULT '0',
  `company` varchar(50) NOT NULL DEFAULT '0',
  `password` char(50) DEFAULT NULL,
  `phone` varchar(50) NOT NULL DEFAULT '0',
  `sendnewsletter` tinyint(4) NOT NULL DEFAULT '1',
  `lastupdate` varchar(40) NOT NULL DEFAULT '',
  `timezone` int(11) NOT NULL,
  `sendalarm` int(11) NOT NULL,
  `alarmtemp` float NOT NULL,
  `alarmtemphigh` float NOT NULL,
  `alarmphone1` varchar(25) NOT NULL,
  `alarmphone2` varchar(25) NOT NULL,
  `alarmemail1` varchar(50) NOT NULL,
  `alarmemail2` varchar(50) NOT NULL,
  `alerttext` varchar(200) NOT NULL,
  `alertcount` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'admin','FirstName','LastName','2001 Hawleyton Road','Binghamton','NY',13903,'Your Company','password','607-724-4828',1,'',0,0,34,95,'6077244828','','mharris@lonemaplefarm.com','mharrisny1@gmail.com','CONNECTION ALERT!!! The Environment: Tomatoes has not reported conditions within the last 30 minutes. IMMEDIATE ACTION is required',0);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `ID` int(11) DEFAULT NULL,
  `name` char(50) DEFAULT NULL,
  `var` char(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'environment','Tomato'),(2,'heater1set1temp','65'),(3,'heatdiff','1.0'),(4,'heater2set1temp','64'),(5,'coolingdiff','1'),(6,'cooling1set1temp','68'),(7,'cooling2set1temp','72'),(8,'cooling3set1temp','74'),(9,'cooling4set1temp','78'),(10,'humidityset1','82'),(11,'serialnum','712110135'),(12,'running','1'),(13,'z1','5'),(14,'z2','5'),(15,'z3','5'),(16,'z4','5'),(17,'z5','5'),(18,'z6','5'),(19,'z7','5'),(20,'z8','5'),(21,'z9','5'),(22,'z10','5'),(23,'molessetpoint','2.5'),(24,'senddata','0'),(25,'timezone','America/New_York'),(26,'alertmintemp','58'),(27,'alertmaxtemp','95'),(28,'heater1set1h','8'),(29,'heater1set1m','30'),(31,'heater1set2h','9'),(32,'heater1set2m','30'),(33,'heater1set2temp','65'),(34,'heater1set2h','11'),(35,'heater1set2m','30'),(36,'heater1set2temp','65'),(37,'c1s1h','0'),(38,'c1s1m','0'),(39,'cooling2set1h','7'),(40,'cooling2set1m','30'),(41,'heater2set1h','7'),(42,'heater2set1m','0'),(43,'cooling3set1h','7'),(44,'cooling3set1m','0'),(45,'cooling4set1h','7'),(46,'cooling4set1m','7'),(47,'version','2'),(48,'upgrade','5'),(49,'restore database','5'),(50,'dailyaccumlight','0.0021608256944444467'),(51,'z14','5'),(52,'z15','5'),(53,'updatetime','0.035388354513889296'),(54,'newdate',''),(55,'newtime',''),(56,'powerdown',''),(57,'c1h','5'),(58,'c1m','00'),(59,'c2h','8'),(60,'c2m','00'),(61,'c3h','11'),(62,'c3m','00'),(63,'c4h','13'),(64,'c4m','00'),(65,'c5h','16'),(66,'c5m','00'),(67,'c6h','18'),(68,'c6m','00'),(69,'c7h','25'),(70,'c7m','00'),(71,'c8h','26'),(72,'c8m','00'),(73,'ipmh','22'),(75,'ipmt','45'),(74,'ipmm','00'),(76,'irrigationbytime','2'),(77,'sensortemp','67.0339018554687'),(78,'sensorrh','14.1911926269531'),(79,'irrigatenow','0'),(80,'irrigating','0'),(81,'singlewatersource','1'),(82,'irrigationrole','0'),(83,'irrigationmasterip','192.168.1.210'),(84,'irrigationmaster','0'),(85,'refreshsettings','0'),(86,'h1s1h','0'),(87,'h1s1m','0'),(88,'h1s2h','8'),(89,'h1s2m','0'),(90,'h1s2t','65'),(91,'h1s3h','10'),(92,'h1s3m','0'),(93,'h1s3t','65'),(94,'h1s4h','12'),(95,'h1s4m','0'),(96,'h1s4t','65'),(97,'h2s1h','0'),(98,'h2s1m','0'),(99,'h2s2h','8'),(100,'h2s2m','0'),(101,'h2s2t','64'),(102,'h2s3h','10'),(103,'h2s3m','0'),(104,'h2s3t','64'),(105,'h2s4h','12'),(106,'h2s4m','0'),(107,'h2s4t','64'),(108,'c1s2h','6'),(109,'c1s2m','0'),(110,'c1s2t','68'),(111,'c1s3h','10'),(112,'c1s3m','0'),(113,'c1s3t','68'),(114,'c1s4h','12'),(115,'c1s4m','0'),(116,'c1s4t','68'),(117,'c2s1h','0'),(118,'c2s1m','0'),(119,'c2s2h','8'),(120,'c2s2m','0'),(121,'c2s2t','70'),(122,'c2s3h','10'),(123,'c2s3m','0'),(124,'c2s3t','70'),(125,'c2s4h','12'),(126,'c2s4m','0'),(127,'c2s4t','70'),(128,'c3s1h','0'),(129,'c3s1m','0'),(130,'c3s2h','8'),(131,'c3s2m','0'),(132,'c3s2t','72'),(133,'c3s3h','10'),(134,'c3s3m','0'),(135,'c3s3t','72'),(136,'c3s4h','12'),(137,'c3s4m','0'),(138,'c3s4t','72'),(139,'c4s1h','0'),(140,'c4s1m','0'),(141,'c4s2h','8'),(142,'c4s2m','0'),(143,'c4s2t','78'),(144,'c4s3h','10'),(145,'c4s3m','0'),(146,'c4s3t','78'),(147,'c4s4h','12'),(148,'c4s4m','0'),(149,'c4s4t','78'),(150,'light','0');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-02 15:50:01
