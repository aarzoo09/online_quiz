-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: onlinequizdb
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `level` varchar(20) DEFAULT NULL,
  `topic` varchar(100) DEFAULT NULL,
  `score` int DEFAULT NULL,
  `total_questions` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `results_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `results`
--

LOCK TABLES `results` WRITE;
/*!40000 ALTER TABLE `results` DISABLE KEYS */;
INSERT INTO `results` VALUES (1,1,'easy','General Knowledge',1,5),(2,1,'easy','General Knowledge',1,5),(3,1,'medium','General Knowledge',0,5),(4,2,'easy','Science',3,5),(5,2,'easy','Mathematics',1,5),(6,1,'easy','General Knowledge',3,5),(7,1,'easy','General Knowledge',4,5),(8,1,'easy','Mathematics',1,5),(9,1,'easy','General Knowledge',2,5),(10,1,'easy','General Knowledge',0,5),(11,1,'easy','General Knowledge',3,5),(12,1,'easy','General Knowledge',3,5),(13,1,'easy','General Knowledge',3,5),(14,1,'easy','General Knowledge',3,5),(15,1,'easy','General Knowledge',3,5),(16,1,'easy','General Knowledge',3,5),(17,1,'easy','General Knowledge',3,5),(18,1,'easy','General Knowledge',3,5),(19,1,'easy','General Knowledge',3,5),(20,1,'easy','General Knowledge',2,5),(21,1,'easy','General Knowledge',2,5),(22,1,'easy','General Knowledge',2,5),(23,1,'easy','General Knowledge',2,5),(24,1,'easy','General Knowledge',1,5),(25,1,'easy','General Knowledge',1,5),(26,1,'easy','General Knowledge',1,5),(27,1,'easy','General Knowledge',1,5),(28,1,'easy','General Knowledge',1,5),(29,1,'easy','General Knowledge',1,5),(30,1,'easy','General Knowledge',1,5),(31,1,'easy','General Knowledge',2,5),(32,1,'easy','General Knowledge',4,5);
/*!40000 ALTER TABLE `results` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-26 16:07:08
