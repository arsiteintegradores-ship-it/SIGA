-- MySQL dump 10.13  Distrib 8.0.28, for macos11 (x86_64)
--
-- Host: localhost    Database: siga_db
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add raza',7,'add_raza'),(26,'Can change raza',7,'change_raza'),(27,'Can delete raza',7,'delete_raza'),(28,'Can view raza',7,'view_raza'),(29,'Can add finca',8,'add_finca'),(30,'Can change finca',8,'change_finca'),(31,'Can delete finca',8,'delete_finca'),(32,'Can view finca',8,'view_finca'),(33,'Can add animal',9,'add_animal'),(34,'Can change animal',9,'change_animal'),(35,'Can delete animal',9,'delete_animal'),(36,'Can view animal',9,'view_animal'),(37,'Can add lote',10,'add_lote'),(38,'Can change lote',10,'change_lote'),(39,'Can delete lote',10,'delete_lote'),(40,'Can view lote',10,'view_lote');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$OpnydLrBU7It9Q2IoZhux3$BFooWeugd1lY75ilF/nBVha7tuaSsusDZYtWkDrjlco=','2026-01-15 15:54:01.674948',1,'Admin','','','igordillo@arsite.com',1,1,'2026-01-15 15:32:33.194425'),(2,'pbkdf2_sha256$600000$gXgSVRq5Gbm9rrCFyPQLVu$ry3GkjdJU5sAhvHSf8DJllIKrJWPoPL83h1vpmOyQkw=',NULL,1,'igordillo','','','igordillo@arsite.com.mx',1,1,'2026-01-15 15:53:00.531751'),(3,'pbkdf2_sha256$600000$QSycBUKa5LyETVzKM7X7pv$ecPlVKVySsBsNTm3Q2L+fxIbNT59L7k+kRU4ZOxmhH0=',NULL,1,'ahernandez','','','amorher@hotmail.com',1,1,'2026-01-15 16:00:00.958207');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-01-15 16:24:37.227655','1','GanadoProductor object (1)',1,'[{\"added\": {}}]',12,1),(2,'2026-01-15 16:25:51.804355','1','GanadoFinca object (1)',1,'[{\"added\": {}}]',13,1),(3,'2026-01-15 16:26:25.145125','1','GanadoColor object (1)',1,'[{\"added\": {}}]',14,1),(4,'2026-01-15 16:27:50.200425','1','GanadoLote object (1)',1,'[{\"added\": {}}]',15,1),(5,'2026-01-15 16:28:33.274011','1','GanadoLote object (1)',2,'[{\"changed\": {\"fields\": [\"Nombre\", \"Descripcion\"]}}]',15,1),(6,'2026-01-15 16:29:03.137739','1','GanadoRaza object (1)',1,'[{\"added\": {}}]',16,1),(7,'2026-01-15 16:32:07.500038','1','GanadoUpp object (1)',1,'[{\"added\": {}}]',17,1),(8,'2026-01-15 21:14:27.100994','1','27845678',2,'[]',17,1),(9,'2026-01-16 02:00:43.976856','2','Rojo',1,'[{\"added\": {}}]',14,1),(10,'2026-01-16 02:03:38.837240','3','Hosco',1,'[{\"added\": {}}]',14,1),(11,'2026-01-16 02:03:56.502901','4','Gateado',1,'[{\"added\": {}}]',14,1),(12,'2026-01-16 02:04:11.815112','5','Pinto',1,'[{\"added\": {}}]',14,1),(13,'2026-01-16 02:04:24.480647','6','Cafe',1,'[{\"added\": {}}]',14,1),(14,'2026-01-16 02:04:36.198958','7','Negro',1,'[{\"added\": {}}]',14,1),(15,'2026-01-16 02:05:14.355843','8','Gris',1,'[{\"added\": {}}]',14,1),(16,'2026-01-16 02:05:28.719633','9','Blanco',1,'[{\"added\": {}}]',14,1),(17,'2026-01-16 02:05:43.448635','10','Cara Blanca',1,'[{\"added\": {}}]',14,1),(18,'2026-01-16 02:06:06.628676','11','Cara Pinta',1,'[{\"added\": {}}]',14,1),(19,'2026-01-16 02:06:31.265095','12','Bragao panza blanca',1,'[{\"added\": {}}]',14,1),(20,'2026-01-16 02:06:52.212714','13','Panza Pinta',1,'[{\"added\": {}}]',14,1),(21,'2026-01-16 02:07:05.375000','14','Ojillos',1,'[{\"added\": {}}]',14,1),(22,'2026-01-16 02:07:16.391626','15','Lucero',1,'[{\"added\": {}}]',14,1),(23,'2026-01-16 02:09:51.831132','2','Los Colibries',1,'[{\"added\": {}}]',13,1),(24,'2026-01-16 02:10:59.157732','2','Suizo',1,'[{\"added\": {}}]',16,1),(25,'2026-01-16 02:11:11.646525','3','Cebu',1,'[{\"added\": {}}]',16,1),(26,'2026-01-16 02:11:22.645124','4','Sardo Negro',1,'[{\"added\": {}}]',16,1),(27,'2026-01-16 02:11:31.905784','5','Nelore',1,'[{\"added\": {}}]',16,1),(28,'2026-01-16 02:12:00.562239','6','Chambray',1,'[{\"added\": {}}]',16,1),(29,'2026-01-16 02:12:50.729850','2','vacias (2)',1,'[{\"added\": {}}]',15,1),(30,'2026-01-16 02:13:29.590836','2','Ada Hernadez Morales',1,'[{\"added\": {}}]',12,1),(31,'2026-01-16 02:14:22.433307','2','987543457',1,'[{\"added\": {}}]',17,1),(32,'2026-01-16 03:00:18.900980','1','100',1,'[{\"added\": {}}]',11,1),(33,'2026-01-16 03:04:15.876262','1','100',2,'[{\"changed\": {\"fields\": [\"Color\"]}}]',11,1),(34,'2026-01-16 03:05:27.956239','1','100',2,'[{\"changed\": {\"fields\": [\"Color\"]}}]',11,1),(35,'2026-01-16 03:06:22.127449','1','100',2,'[{\"changed\": {\"fields\": [\"Color\"]}}]',11,1),(36,'2026-01-16 03:06:52.815428','1','100',2,'[{\"changed\": {\"fields\": [\"Raza\"]}}]',11,1),(37,'2026-01-16 03:26:00.777171','2','501',1,'[{\"added\": {}}]',11,1),(38,'2026-01-16 03:29:14.741911','3','Sementales (1)',1,'[{\"added\": {}}]',15,1),(39,'2026-01-16 03:30:27.758210','3','500',1,'[{\"added\": {}}]',11,1),(40,'2026-01-16 03:32:08.269426','3','keyla Sarai Garcia Hernandez',1,'[{\"added\": {}}]',12,1),(41,'2026-01-16 03:32:52.095766','2','501',2,'[{\"changed\": {\"fields\": [\"Productor\"]}}]',11,1),(42,'2026-01-16 04:37:04.920687','4','300',1,'[{\"added\": {}}]',11,1),(43,'2026-01-16 06:15:59.206255','1','100',3,'',11,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(9,'ganado','animal'),(8,'ganado','finca'),(11,'ganado','ganadoanimal'),(14,'ganado','ganadocolor'),(13,'ganado','ganadofinca'),(15,'ganado','ganadolote'),(12,'ganado','ganadoproductor'),(16,'ganado','ganadoraza'),(18,'ganado','ganadoregistro'),(17,'ganado','ganadoupp'),(10,'ganado','lote'),(7,'ganado','raza'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-01-15 15:31:12.752879'),(2,'auth','0001_initial','2026-01-15 15:31:13.215382'),(3,'admin','0001_initial','2026-01-15 15:31:13.323014'),(4,'admin','0002_logentry_remove_auto_add','2026-01-15 15:31:13.336327'),(5,'admin','0003_logentry_add_action_flag_choices','2026-01-15 15:31:13.353751'),(6,'contenttypes','0002_remove_content_type_name','2026-01-15 15:31:13.449977'),(7,'auth','0002_alter_permission_name_max_length','2026-01-15 15:31:13.502946'),(8,'auth','0003_alter_user_email_max_length','2026-01-15 15:31:13.540029'),(9,'auth','0004_alter_user_username_opts','2026-01-15 15:31:13.553577'),(10,'auth','0005_alter_user_last_login_null','2026-01-15 15:31:13.610692'),(11,'auth','0006_require_contenttypes_0002','2026-01-15 15:31:13.614638'),(12,'auth','0007_alter_validators_add_error_messages','2026-01-15 15:31:13.627948'),(13,'auth','0008_alter_user_username_max_length','2026-01-15 15:31:13.681800'),(14,'auth','0009_alter_user_last_name_max_length','2026-01-15 15:31:13.739563'),(15,'auth','0010_alter_group_name_max_length','2026-01-15 15:31:13.768900'),(16,'auth','0011_update_proxy_permissions','2026-01-15 15:31:13.783313'),(17,'auth','0012_alter_user_first_name_max_length','2026-01-15 15:31:13.910833'),(18,'sessions','0001_initial','2026-01-15 15:49:10.366640'),(19,'ganado','0001_initial','2026-01-15 15:49:41.336977');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0z78k5915bt7s4vhh467tgcz6a8hic7o','.eJxVjEEOwiAQRe_C2hAGhIJL956BDDOjVA1NSrsy3l2bdKHb_977L5VxXWpeu8x5ZHVSoA6_W0F6SNsA37HdJk1TW-ax6E3RO-36MrE8z7v7d1Cx12-NZMAKBScowAwmGG-5lHQcQohElMxVEogtzkXvBoaQvC1so00xGlDvD-3uN2s:1vgPfd:KCqjHqEp9nRdXvKcLQ1_8qXQ8F6psl1I3vpb_hvWhiw','2026-01-29 15:54:01.680853');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganado_animal`
--

DROP TABLE IF EXISTS `ganado_animal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ganado_animal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_interno` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_siniga` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nombre_bov` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `peso_nacimiento` decimal(6,2) DEFAULT NULL,
  `peso_destete` decimal(6,2) DEFAULT NULL,
  `productor_id` int DEFAULT NULL,
  `upp_id` int DEFAULT NULL,
  `color_id` int DEFAULT NULL,
  `raza_id` int DEFAULT NULL,
  `registro_id` int DEFAULT NULL,
  `sexo` enum('M','H') COLLATE utf8mb4_unicode_ci NOT NULL,
  `padre_id` int DEFAULT NULL,
  `madre_id` int DEFAULT NULL,
  `finca_id` int NOT NULL,
  `lote_id` int DEFAULT NULL,
  `estado` enum('ACTIVO','VENDIDO','MUERTO','BAJA') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVO',
  `notas` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_interno` (`id_interno`),
  UNIQUE KEY `id_siniga` (`id_siniga`),
  KEY `idx_animal_finca` (`finca_id`),
  KEY `idx_animal_lote` (`lote_id`),
  KEY `idx_animal_raza` (`raza_id`),
  KEY `idx_animal_padre` (`padre_id`),
  KEY `idx_animal_madre` (`madre_id`),
  KEY `fk_ganado_animal_productor` (`productor_id`),
  KEY `fk_ganado_animal_upp` (`upp_id`),
  KEY `fk_ganado_animal_color` (`color_id`),
  KEY `fk_ganado_animal_registro` (`registro_id`),
  CONSTRAINT `fk_ganado_animal_color` FOREIGN KEY (`color_id`) REFERENCES `ganado_color` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_animal_finca` FOREIGN KEY (`finca_id`) REFERENCES `ganado_finca` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_animal_lote` FOREIGN KEY (`lote_id`) REFERENCES `ganado_lote` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_animal_madre` FOREIGN KEY (`madre_id`) REFERENCES `ganado_animal` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_animal_padre` FOREIGN KEY (`padre_id`) REFERENCES `ganado_animal` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_animal_productor` FOREIGN KEY (`productor_id`) REFERENCES `ganado_productor` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_animal_raza` FOREIGN KEY (`raza_id`) REFERENCES `ganado_raza` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_animal_registro` FOREIGN KEY (`registro_id`) REFERENCES `ganado_registro` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_animal_upp` FOREIGN KEY (`upp_id`) REFERENCES `ganado_upp` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganado_animal`
--

LOCK TABLES `ganado_animal` WRITE;
/*!40000 ALTER TABLE `ganado_animal` DISABLE KEYS */;
INSERT INTO `ganado_animal` VALUES (2,'501','2234234234456','Berenice','2026-01-16',20.00,30.00,3,1,12,6,NULL,'H',NULL,NULL,2,2,'ACTIVO','dfgsrgseddfg','2026-01-16 03:26:01','2026-01-16 03:32:52'),(3,'500','588778786','Thor','2026-01-16',56.00,78.00,2,2,3,1,NULL,'M',NULL,NULL,1,3,'ACTIVO','semenyal con caracteristica sorprendes','2026-01-16 03:30:28','2026-01-16 03:30:28'),(4,'300','5675675675','terry','2026-01-16',45.00,34.00,1,2,10,6,NULL,'M',NULL,40,2,NULL,'ACTIVO','egsdhsrsntyjntyjt','2026-01-16 04:37:05','2026-01-16 06:13:50'),(5,'101','2718363154',NULL,'2024-12-14',34.00,NULL,4,3,NULL,7,NULL,'H',NULL,6,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(6,'102','2717353199','Dulce','2023-01-27',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,11,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(7,'103','2717933193','Becky','2023-01-18',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,15,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(8,'104','2715218410','Chikis','2015-06-06',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(9,'105','2714948637','Popis','2019-08-15',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(10,'106','Sin Sinniga',NULL,'2025-10-17',32.00,NULL,4,3,NULL,8,NULL,'H',NULL,18,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(11,'107','2715218405','Jarocha','2019-01-10',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(12,'108','2716121864','Cukis','2021-04-16',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(13,'110','2718363152',NULL,'2024-12-15',36.00,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(14,'111','2715170822','Clara','2017-08-15',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(15,'115','2714941095','Galilea','2018-11-02',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(16,'116','2717353211','Luisa','2021-07-15',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(17,'117','2715512916','Gatita','2020-04-16',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(18,'119','3074711255','Veracruzana','2021-02-14',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(19,'122','2714762409','Rubi','2019-01-05',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(20,'131','2717933211','Berenise','2023-09-30',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(21,'133','2717933192','Desire','2023-12-28',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,19,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(22,'134','2717284912','Vivian','2022-11-12',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(23,'139','2717284909','Yisel','2022-12-12',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(24,'140','2717284915','Carolina','2022-10-12',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(25,'142','2717284913','Soqui','2022-10-10',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(26,'143','2717284919','Anabel','2022-11-05',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(27,'147','2717933205','Bibi','2024-03-27',NULL,NULL,4,3,NULL,7,NULL,'H',NULL,12,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(28,'175','3074711253','Bruja','2021-02-10',NULL,NULL,4,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:49'),(29,'190','2717933195','Zeus','2023-08-31',NULL,NULL,4,3,NULL,8,NULL,'M',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(30,'302','2718363158','Rasputin','2024-08-09',33.00,NULL,4,3,NULL,8,NULL,'M',NULL,53,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(31,'303','2718363156','Kaliman','2024-08-18',32.00,NULL,4,3,NULL,8,NULL,'M',NULL,28,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:49','2026-01-16 06:13:50'),(32,'304','2717933202','Thor','2024-06-14',NULL,NULL,4,3,NULL,8,NULL,'M',NULL,22,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(33,'502','2718363157','Dalila','2024-07-17',35.00,NULL,5,3,NULL,8,NULL,'H',NULL,59,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(34,'503','2714941078','Atenea','2019-05-10',NULL,NULL,5,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(35,'504','2715170827','Panchita','2018-07-04',NULL,NULL,5,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(36,'505','2715170824','Jimena','2018-01-15',NULL,NULL,5,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(37,'507','2714948602','Afrodita','2018-08-10',NULL,NULL,5,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(38,'509','2713883045','Paulina','2017-06-10',NULL,NULL,5,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(39,'510','2715512912','Artemisa','2020-04-01',NULL,NULL,5,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(40,'511','2714948641','Estrella','2019-06-10',NULL,NULL,5,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(41,'512','2718363160',NULL,'2024-12-27',33.00,NULL,5,3,NULL,8,NULL,'H',NULL,39,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(42,'516','3071651264',NULL,'2019-11-20',NULL,NULL,5,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(43,'517','2718363161',NULL,'2024-12-03',35.00,NULL,5,3,NULL,8,NULL,'H',NULL,48,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(44,'519','2717284911','Perla','2022-10-02',NULL,NULL,5,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(45,'522','2717284914','Pamela','2022-10-12',NULL,NULL,5,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(46,'525','2717933201','Mikaela','2024-04-12',NULL,NULL,5,3,NULL,8,NULL,'H',NULL,37,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(47,'527','2717933199','Pricila','2023-07-09',NULL,NULL,5,3,NULL,8,NULL,'H',NULL,37,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(48,'587','3074711251','Brisa','2021-02-10',NULL,NULL,5,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(49,'591','2718363153',NULL,'2024-12-06',34.00,NULL,5,3,NULL,7,NULL,'M',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(50,'600','2717353212','Margarita','2021-07-15',NULL,NULL,6,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(51,'601','2715218417','Bella','2019-12-15',NULL,NULL,6,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(52,'602','2716646005','Safiro','2018-06-25',NULL,NULL,6,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(53,'605','2715512935','Aurora','2020-04-20',NULL,NULL,6,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(54,'606','2715907234','Jade','2020-03-15',NULL,NULL,6,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(55,'607','2716646001','Wanda','2022-04-09',NULL,NULL,6,3,NULL,8,NULL,'H',NULL,58,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(56,'609','2717353218','Raquel','2022-10-31',NULL,NULL,6,4,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(57,'612','2715512669','Nina','2019-12-12',NULL,NULL,6,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(58,'615','2714941043','Mulan','2019-06-07',NULL,NULL,6,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(59,'616','3075749961','Marina','2023-03-04',NULL,NULL,6,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(60,'617','2717933203','Mariana','2024-04-05',NULL,NULL,6,3,NULL,8,NULL,'H',NULL,58,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:51'),(61,'621','2718363155','Muñeca','2024-06-19',33.00,NULL,6,3,NULL,8,NULL,'H',NULL,57,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:51'),(62,'700','369624','Rambo','2022-02-14',NULL,NULL,7,3,NULL,8,NULL,'M',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(63,'701','2715218412','Silvia','2014-05-15',NULL,NULL,7,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(64,'703','2715170828','Yesenia','2018-04-15',NULL,NULL,7,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(65,'706','2716121868','Kristel','2021-10-05',NULL,NULL,7,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(66,'707','2715907241','Vianca','2020-08-20',NULL,NULL,7,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(67,'708','2715907230','Sasu','2020-09-15',NULL,NULL,7,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(68,'711','2715512601','Sasha','2020-01-06',NULL,NULL,7,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(69,'715','2714948642','Shakira','2019-06-15',NULL,NULL,7,3,NULL,8,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(70,'716','2717933214','Pandora','2024-05-13',NULL,NULL,7,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:51'),(71,'720','2717933187','Poseidon','2023-11-13',NULL,NULL,7,3,NULL,8,NULL,'M',NULL,68,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:51'),(72,'791','2718363145',NULL,'2025-01-15',34.00,NULL,7,3,NULL,7,NULL,'M',NULL,63,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:51'),(73,'793','2718363151',NULL,'2024-12-12',35.00,NULL,7,3,NULL,7,NULL,'M',NULL,67,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:51'),(74,'800','2714894380','AddyFlor','2019-04-15',NULL,NULL,8,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(75,'801','2717353210','Rosa','2021-06-20',NULL,NULL,8,3,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:50'),(76,'802','2717353208','Olivia','2023-04-14',NULL,NULL,9,4,NULL,7,NULL,'H',NULL,54,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:51'),(77,'803','2717353217','Lassie','2022-11-19',NULL,NULL,9,4,NULL,7,NULL,'H',NULL,NULL,1,NULL,'ACTIVO',NULL,'2026-01-16 06:13:50','2026-01-16 06:13:51');
/*!40000 ALTER TABLE `ganado_animal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganado_color`
--

DROP TABLE IF EXISTS `ganado_color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ganado_color` (
  `id` int NOT NULL AUTO_INCREMENT,
  `color` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `color` (`color`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganado_color`
--

LOCK TABLES `ganado_color` WRITE;
/*!40000 ALTER TABLE `ganado_color` DISABLE KEYS */;
INSERT INTO `ganado_color` VALUES (1,'Bayo','2026-01-15 16:26:21','2026-01-15 16:26:24'),(2,'Rojo','2026-01-16 02:00:38','2026-01-16 02:00:42'),(3,'Hosco','2026-01-16 02:03:34','2026-01-16 02:03:36'),(4,'Gateado','2026-01-16 02:03:51','2026-01-16 02:03:54'),(5,'Pinto','2026-01-16 02:04:04','2026-01-16 02:04:08'),(6,'Cafe','2026-01-16 02:04:21','2026-01-16 02:04:23'),(7,'Negro','2026-01-16 02:04:31','2026-01-16 02:04:34'),(8,'Gris','2026-01-16 02:04:55','2026-01-16 02:04:57'),(9,'Blanco','2026-01-16 02:05:25','2026-01-16 02:05:27'),(10,'Cara Blanca','2026-01-16 02:05:40','2026-01-16 02:05:42'),(11,'Cara Pinta','2026-01-16 02:06:03','2026-01-16 02:06:05'),(12,'Bragao panza blanca','2026-01-16 02:06:28','2026-01-16 02:06:30'),(13,'Panza Pinta','2026-01-16 02:06:47','2026-01-16 02:06:49'),(14,'Ojillos','2026-01-16 02:07:02','2026-01-16 02:07:04'),(15,'Lucero','2026-01-16 02:07:13','2026-01-16 02:07:15');
/*!40000 ALTER TABLE `ganado_color` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganado_finca`
--

DROP TABLE IF EXISTS `ganado_finca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ganado_finca` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ubicacion` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hectareas` decimal(10,2) DEFAULT NULL,
  `propietario` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganado_finca`
--

LOCK TABLES `ganado_finca` WRITE;
/*!40000 ALTER TABLE `ganado_finca` DISABLE KEYS */;
INSERT INTO `ganado_finca` VALUES (1,'Las Adas','La Estrella',16.00,'Isaias Garcia Gordillo','9933939655',1,'2026-01-15 16:25:46','2026-01-15 16:25:48'),(2,'Los Colibries','La Estrella',16.00,'Isaias Garcia Gordillo','9933939655',1,'2026-01-16 02:09:45','2026-01-16 02:09:49');
/*!40000 ALTER TABLE `ganado_finca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganado_lote`
--

DROP TABLE IF EXISTS `ganado_lote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ganado_lote` (
  `id` int NOT NULL AUTO_INCREMENT,
  `finca_id` int NOT NULL,
  `nombre` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_lote_finca_nombre` (`finca_id`,`nombre`),
  KEY `idx_lote_finca` (`finca_id`),
  CONSTRAINT `fk_ganado_lote_finca` FOREIGN KEY (`finca_id`) REFERENCES `ganado_finca` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganado_lote`
--

LOCK TABLES `ganado_lote` WRITE;
/*!40000 ALTER TABLE `ganado_lote` DISABLE KEYS */;
INSERT INTO `ganado_lote` VALUES (1,1,'Preñadas','Pie de Cria  cargadas',1,'2026-01-15 16:27:44','2026-01-15 16:27:47'),(2,2,'vacias','Lote de Vacas Vacias',1,'2026-01-16 02:12:46','2026-01-16 02:12:48'),(3,1,'Sementales','Lote de Sementales',1,'2026-01-16 03:29:09','2026-01-16 03:29:12');
/*!40000 ALTER TABLE `ganado_lote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganado_productor`
--

DROP TABLE IF EXISTS `ganado_productor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ganado_productor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido_paterno` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `apellido_materno` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_productor_nombre` (`nombre`,`apellido_paterno`,`apellido_materno`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganado_productor`
--

LOCK TABLES `ganado_productor` WRITE;
/*!40000 ALTER TABLE `ganado_productor` DISABLE KEYS */;
INSERT INTO `ganado_productor` VALUES (1,'Isaias','Garcia','Gordillo','Calle Musicos 714, Col. Gaviotas Sur','9933939655','Igordillo@arsite.com.mx',1,'2026-01-15 16:24:34','2026-01-15 16:24:35'),(2,'Ada','Hernadez','Morales','Calle Musicos 714, Col. Gaviotas Sur','9933939677','Igordillo@arsite.com.mx',1,'2026-01-16 02:13:25','2026-01-16 02:13:27'),(3,'keyla Sarai','Garcia','Hernandez','Calle Musicos 714, Col. Gaviotas Sur','9933939655','Igordillo@arsite.com.mx',1,'2026-01-16 03:32:03','2026-01-16 03:32:05'),(4,'ISAÍAS',NULL,NULL,NULL,NULL,NULL,1,'2026-01-16 06:11:00','2026-01-16 06:11:00'),(5,'ADA',NULL,NULL,NULL,NULL,NULL,1,'2026-01-16 06:11:00','2026-01-16 06:11:00'),(6,'KEYLA',NULL,NULL,NULL,NULL,NULL,1,'2026-01-16 06:11:01','2026-01-16 06:11:01'),(7,'SOFIA',NULL,NULL,NULL,NULL,NULL,1,'2026-01-16 06:11:01','2026-01-16 06:11:01'),(8,'ADYFLOR',NULL,NULL,NULL,NULL,NULL,1,'2026-01-16 06:11:01','2026-01-16 06:11:01'),(9,'ADDYFLOR',NULL,NULL,NULL,NULL,NULL,1,'2026-01-16 06:11:01','2026-01-16 06:11:01');
/*!40000 ALTER TABLE `ganado_productor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganado_raza`
--

DROP TABLE IF EXISTS `ganado_raza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ganado_raza` (
  `id` int NOT NULL AUTO_INCREMENT,
  `raza` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `raza` (`raza`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganado_raza`
--

LOCK TABLES `ganado_raza` WRITE;
/*!40000 ALTER TABLE `ganado_raza` DISABLE KEYS */;
INSERT INTO `ganado_raza` VALUES (1,'Beffmaster','2026-01-15 16:28:58','2026-01-15 16:29:01'),(2,'Suizo','2026-01-16 02:10:55','2026-01-16 02:10:57'),(3,'Cebu','2026-01-16 02:11:07','2026-01-16 02:11:08'),(4,'Sardo Negro','2026-01-16 02:11:19','2026-01-16 02:11:21'),(5,'Nelore','2026-01-16 02:11:28','2026-01-16 02:11:30'),(6,'Chambray','2026-01-16 02:11:58','2026-01-16 02:11:59'),(7,'Cruza','2026-01-16 06:11:00','2026-01-16 06:11:00'),(8,'Beefmaster','2026-01-16 06:11:00','2026-01-16 06:11:00'),(9,'TE-Beefmaster','2026-01-16 06:11:00','2026-01-16 06:11:00');
/*!40000 ALTER TABLE `ganado_raza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganado_registro`
--

DROP TABLE IF EXISTS `ganado_registro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ganado_registro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_madre` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_padre` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_abuelo` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_abuela` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_bovino` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_registro_bovino` (`id_bovino`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganado_registro`
--

LOCK TABLES `ganado_registro` WRITE;
/*!40000 ALTER TABLE `ganado_registro` DISABLE KEYS */;
/*!40000 ALTER TABLE `ganado_registro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ganado_upp`
--

DROP TABLE IF EXISTS `ganado_upp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ganado_upp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `finca_id` int NOT NULL,
  `productor_id` int NOT NULL,
  `clave` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clave` (`clave`),
  KEY `idx_upp_finca` (`finca_id`),
  KEY `idx_upp_productor` (`productor_id`),
  CONSTRAINT `fk_ganado_upp_finca` FOREIGN KEY (`finca_id`) REFERENCES `ganado_finca` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_ganado_upp_productor` FOREIGN KEY (`productor_id`) REFERENCES `ganado_productor` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ganado_upp`
--

LOCK TABLES `ganado_upp` WRITE;
/*!40000 ALTER TABLE `ganado_upp` DISABLE KEYS */;
INSERT INTO `ganado_upp` VALUES (1,1,1,'27845678','2026-01-15 16:31:58','2026-01-15 16:32:06'),(2,2,2,'987543457','2026-01-16 02:14:18','2026-01-16 02:14:21'),(3,1,8,'27-003-7620-001','2026-01-16 06:11:00','2026-01-16 06:13:50'),(4,1,9,'27-003-1316-002','2026-01-16 06:11:01','2026-01-16 06:13:50');
/*!40000 ALTER TABLE `ganado_upp` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-16  7:16:29
