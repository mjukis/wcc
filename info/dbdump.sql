-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: wcc
-- ------------------------------------------------------
-- Server version	5.5.41-0+wheezy1

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
-- Table structure for table `eventlist`
--

DROP TABLE IF EXISTS `eventlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eventlist` (
  `id` varchar(10) NOT NULL,
  `name` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventlist`
--

LOCK TABLES `eventlist` WRITE;
/*!40000 ALTER TABLE `eventlist` DISABLE KEYS */;
INSERT INTO `eventlist` VALUES ('2412001500','Gate Opens'),('2418451500','Main Stage - Opening Ceremonies'),('2419005500','Grimace'),('2419303500','Burning Sands Warriors @ Main Stage'),('2420307500','Burning Sands Warriors @ Main Stage'),('2422007500','Nuclear Bombshells of Lost Vegas @ Main Stage'),('2511003250','Caravan Tournament @ Last Chance Casino'),('2511003500','Archery Practice'),('2511007500','Main Stage - Music'),('2514001500','Open Vehicle Cruise'),('2515003500','Smashbotz RC Car Wars'),('2516001500','Jugger Match'),('2517009500','Tribe Group Photos @ Gate'),('2519005500','Many Of Odd Nature'),('2520007500','Wasteland Fashion Show @ Main Stage'),('2520307500','Burning Sands Warriors @ Main Stage'),('2521005500','AHTCK'),('2522007500','Nuclear Bombshells of Lost Vegas @ Main Stage'),('2523005500','Cage9'),('2523457500','Burning Sensations @ Main Stage'),('2603009500','STFU'),('2611003500','Archery Contest'),('2614001500','Car Contest Judging'),('2614151500','Car Contest Cruise'),('2615001500','Car Contest Prize Ceremony'),('2616001500','Jugger Match'),('2616307500','Wasteland Costume Contest @ Main Stage'),('2617451500','Official Group Photo @ Gate'),('2618303500','Smashbotz'),('2619305500','7 Days Away'),('2619309500','Raffle Winners Announced'),('2620307500','Nuclear Bombshells of Lost Vegas @ Main Stage'),('2621005500','A440'),('2622007500','Sin City Belly Dance @ Main Stage'),('2700005500','Aesthetic Meat Front'),('2700303500','Last Chance Casino Final Auction'),('2700457500','Burning Sensations @ Main Stage'),('2703009500','STFU'),('2711001500','Brother Justify @ The Temple Of The Nuke'),('2712003500','Wasteland Rocket Launch'),('2712009500','Event Ends :((('),('2809001500','TEST EVENT 0900'),('2815001500','TEST EVENT 2100'),('2900000500','MIDNIGHT'),('2900101500','TEST EVENT 0010'),('2902001500','TEST EVENT 0200');
/*!40000 ALTER TABLE `eventlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hours`
--

DROP TABLE IF EXISTS `hours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hours` (
  `name` tinytext,
  `day` varchar(2) DEFAULT NULL,
  `open` varchar(4) DEFAULT NULL,
  `close` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hours`
--

LOCK TABLES `hours` WRITE;
/*!40000 ALTER TABLE `hours` DISABLE KEYS */;
INSERT INTO `hours` VALUES ('Post Office','24','1200','1800'),('Post Office','25','1000','1800'),('Post Office','26','1000','1800'),('Post Office','27','0900','1100'),('Atomic Cafe','24','1845','2530'),('Atomic Cafe','25','1845','2600'),('Atomic Cafe','26','1900','2630'),('Wasteland Theater','24','1930','2530'),('Wasteland Theater','25','1930','2530'),('Wasteland Theater','26','1930','2700'),('Main Stage','24','1845','2500'),('Main Stage','25','1100','2530'),('Main Stage','26','1100','2630'),('The PIT','24','1845','2600'),('The PIT','25','1845','2630'),('The PIT','26','1900','2700'),('Last Chance Casino','24','1800','2350'),('Last Chance Casino','25','1800','2350'),('Last Chance Casino','26','1800','2350'),('Body Shop','24','1200','1800'),('Body Shop','25','1000','1800'),('Body Shop','26','1000','1800');
/*!40000 ALTER TABLE `hours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radiolist`
--

DROP TABLE IF EXISTS `radiolist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radiolist` (
  `id` varchar(10) NOT NULL,
  `name` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radiolist`
--

LOCK TABLES `radiolist` WRITE;
/*!40000 ALTER TABLE `radiolist` DISABLE KEYS */;
INSERT INTO `radiolist` VALUES ('240855','Wake Up Wasteland'),('240900','The Morning Fallout'),('241100','Morning News'),('241105','Regular Programming'),('241800','Evening News'),('241805','Sunset Soundtracks'),('241900','Regular Programming'),('250300','The Last Last Call'),('250305','Nuclear Winter'),('250855','Wake Up Wasteland'),('250900','The Morning Fallout'),('251100','Morning News'),('251105','Regular Programming'),('251800','Evening News'),('251805','Sunset Soundtracks'),('251900','Regular Programming'),('260300','The Last Last Call'),('260305','Nuclear Winter'),('260855','Wake Up Wasteland'),('260900','The Morning Fallout'),('261100','Morning News'),('261105','Regular Programming'),('261800','Evening News'),('261805','Sunset Soundtracks'),('261900','Regular Programming'),('270300','The Last Last Call'),('270305','Nuclear Winter'),('270855','Wake Up Wasteland'),('270900','The Morning Fallout'),('271100','Morning News'),('271105','Regular Programming'),('271200','The End Of The World');
/*!40000 ALTER TABLE `radiolist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-03-15 22:53:14
