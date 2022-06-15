-- MySQL dump 10.13  Distrib 5.7.34, for Win64 (x86_64)
--
-- Host: localhost    Database: pharma
-- ------------------------------------------------------
-- Server version	5.5.5-10.3.27-MariaDB-0+deb10u1

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
-- Table structure for table `data_reactor1`
--

DROP TABLE IF EXISTS `data_reactor1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_reactor1` (
  `idreactor1data` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `recording_id` int(11) NOT NULL,
  `time` bigint(20) DEFAULT NULL,
  `datetime` datetime DEFAULT current_timestamp(),
  `press_system` decimal(5,2) DEFAULT NULL,
  `press_flowsyna` decimal(5,2) DEFAULT NULL,
  `press_flowsynb` decimal(5,2) DEFAULT NULL,
  `press_binaryc` decimal(5,2) DEFAULT NULL,
  `press_binaryd` decimal(5,2) DEFAULT NULL,
  `temp_reactor1` decimal(5,2) DEFAULT NULL,
  `temp_reactor2` decimal(5,2) DEFAULT NULL,
  `temp_reactor3` decimal(5,2) unsigned zerofill DEFAULT NULL,
  `temp_reactor4` decimal(5,2) DEFAULT NULL,
  `valve_synvalvea` tinyint(4) DEFAULT NULL,
  `valve_synvalveb` tinyint(4) DEFAULT NULL,
  `valve_binaryvalvec` tinyint(4) DEFAULT NULL,
  `valve_binaryvalved` tinyint(4) DEFAULT NULL,
  `valve_syninjvalvea` tinyint(4) DEFAULT NULL,
  `valve_syninjvalveb` tinyint(4) DEFAULT NULL,
  `valve_binaryinjvalvec` tinyint(4) DEFAULT NULL,
  `valve_binaryinjvalved` tinyint(4) DEFAULT NULL,
  `valve_cw` tinyint(4) DEFAULT NULL,
  `flow_pumpa` decimal(5,2) DEFAULT NULL,
  `flow_pumpb` decimal(5,2) DEFAULT NULL,
  `flow_pumpc` decimal(5,2) DEFAULT NULL,
  `flow_pumpd` decimal(5,2) DEFAULT NULL,
  `chiller_detected` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`idreactor1data`),
  UNIQUE KEY `idreactor1data_UNIQUE` (`idreactor1data`)
) ENGINE=InnoDB AUTO_INCREMENT=1006157 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_reactor1`
--

LOCK TABLES `data_reactor1` WRITE;
/*!40000 ALTER TABLE `data_reactor1` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_reactor1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dbasename`
--

DROP TABLE IF EXISTS `dbasename`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dbasename` (
  `idtest` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data1` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data2` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`idtest`),
  UNIQUE KEY `idtest_UNIQUE` (`idtest`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dbasename`
--

LOCK TABLES `dbasename` WRITE;
/*!40000 ALTER TABLE `dbasename` DISABLE KEYS */;
/*!40000 ALTER TABLE `dbasename` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recordings`
--

DROP TABLE IF EXISTS `recordings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recordings` (
  `idrecordings` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `time` bigint(20) NOT NULL,
  `datetime` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`idrecordings`),
  UNIQUE KEY `idrecordings_UNIQUE` (`idrecordings`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recordings`
--

LOCK TABLES `recordings` WRITE;
/*!40000 ALTER TABLE `recordings` DISABLE KEYS */;
/*!40000 ALTER TABLE `recordings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'pharma'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-09-10 14:29:05
