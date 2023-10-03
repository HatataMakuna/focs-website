-- --------------------------------------------------------
-- Host:                         focs-website.c1efdodxxtlq.us-east-1.rds.amazonaws.com
-- Server version:               10.6.14-MariaDB - managed by https://aws.amazon.com/rds/
-- Server OS:                    Linux
-- HeidiSQL Version:             12.5.0.6677
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for focs-website
DROP DATABASE IF EXISTS `focs-website`;
CREATE DATABASE IF NOT EXISTS `focs-website` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_bin */;
USE `focs-website`;

-- Dumping structure for table focs-website.campus
DROP TABLE IF EXISTS `campus`;
CREATE TABLE IF NOT EXISTS `campus` (
  `abbr` char(2) NOT NULL,
  `desc` varchar(50) NOT NULL,
  `programme_id` int(11) NOT NULL,
  PRIMARY KEY (`abbr`,`programme_id`),
  KEY `FK_campus_programme` (`programme_id`),
  CONSTRAINT `FK_campus_programme` FOREIGN KEY (`programme_id`) REFERENCES `programme` (`programme_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.campus: ~0 rows (approximately)

-- Dumping structure for table focs-website.chatbot_session
DROP TABLE IF EXISTS `chatbot_session`;
CREATE TABLE IF NOT EXISTS `chatbot_session` (
  `ip_addr` varchar(50) NOT NULL,
  `id` char(36) NOT NULL DEFAULT '',
  `created_at` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ip_addr`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.chatbot_session: ~5 rows (approximately)
INSERT INTO `chatbot_session` (`ip_addr`, `id`, `created_at`) VALUES
	('127.0.0.1', '6f69da42-dbf4-40ca-8ddf-61d2e6836ed0', 1695955768),
	('180.74.67.212', '93567873-4249-40e2-ac16-80b2e96d902a', 1695956169),
	('192.168.0.101', '84ee6080-c40c-41a6-9b57-c11c60d7bbc9', 1695952054),
	('210.186.196.224', '396d5d65-93a4-478c-a5a7-ed329038defe', 1695902241),
	('210.186.196.231', '37ef6468-2961-43d1-925d-6d9d8c015f3b', 1695955449);

-- Dumping structure for table focs-website.ip_addr
DROP TABLE IF EXISTS `ip_addr`;
CREATE TABLE IF NOT EXISTS `ip_addr` (
  `value` varchar(50) NOT NULL,
  `enter_count` smallint(5) unsigned NOT NULL DEFAULT 1,
  `first_enter_at` int(10) unsigned NOT NULL DEFAULT 0,
  `unblock_at` int(10) unsigned NOT NULL DEFAULT 0,
  `block_count` int(10) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`value`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.ip_addr: ~20 rows (approximately)
INSERT INTO `ip_addr` (`value`, `enter_count`, `first_enter_at`, `unblock_at`, `block_count`) VALUES
	('103.130.13.169', 1, 1695609206, 0, 0),
	('115.164.182.245', 1, 1695956703, 0, 0),
	('127.0.0.1', 2, 1695955806, 0, 0),
	('180.74.67.104', 1, 1695127272, 0, 0),
	('180.74.67.119', 1, 1695130222, 0, 0),
	('180.74.67.212', 1, 1695956235, 0, 0),
	('185.142.236.43', 1, 1695123816, 0, 0),
	('192.168.0.101', 1, 1695954737, 0, 0),
	('192.168.0.108', 1, 1695399821, 0, 0),
	('192.168.0.112', 1, 1695553320, 0, 0),
	('194.180.48.50', 1, 1695955865, 0, 0),
	('202.184.23.243', 3, 1695955553, 0, 0),
	('210.186.196.159', 1, 1695954424, 0, 0),
	('210.186.196.224', 4, 1695906352, 0, 0),
	('210.186.196.231', 3, 1695956278, 0, 0),
	('210.187.145.60', 1, 1695954423, 0, 0),
	('45.88.90.116', 1, 1695956024, 0, 0),
	('47.254.16.187', 1, 1695904027, 0, 0),
	('47.254.76.138', 1, 1695904026, 0, 0),
	('47.88.101.3', 1, 1695904027, 0, 0);

-- Dumping structure for table focs-website.job
DROP TABLE IF EXISTS `job`;
CREATE TABLE IF NOT EXISTS `job` (
  `value` varchar(50) NOT NULL,
  `programme_id` int(11) NOT NULL,
  PRIMARY KEY (`value`,`programme_id`),
  KEY `FK_job_programme` (`programme_id`),
  CONSTRAINT `FK_job_programme` FOREIGN KEY (`programme_id`) REFERENCES `programme` (`programme_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.job: ~0 rows (approximately)

-- Dumping structure for table focs-website.programmes
DROP TABLE IF EXISTS `programmes`;
CREATE TABLE IF NOT EXISTS `programmes` (
  `id` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.programmes: ~18 rows (approximately)
INSERT INTO `programmes` (`id`, `name`) VALUES
	('dcs', 'Diploma in Computer Science'),
	('dft', 'Diploma in Information Technology'),
	('dis', 'Diploma in Information Systems'),
	('dse', 'Diploma in Software Engineering'),
	('mcs', 'Master of Computer Science'),
	('mit', 'Master of Information Technology'),
	('mms', 'Master of Science in Mathematical Sciences'),
	('pcs', 'Doctor of Philosophy (Computer Science)'),
	('pit', 'Doctor of Philosophy (Information Technology)'),
	('pms', 'Doctor of Philosophy (Mathematical Sciences)'),
	('rds', 'Bachelor of Computer Science (Honours) in Data Science'),
	('rei', 'Bachelor of Information Systems (Honours) in Enterprise Information Systems'),
	('ris', 'Bachelor of Information Technology (Honours) in Information Security'),
	('rit', 'Bachelor of Information Technology (Honours) in Internet Technology'),
	('rmm', 'Bachelor of Science (Honours) in Managment Mathematics with Computing'),
	('rsd', 'Bachelor of Information Technology (Honours) in Software Systems Development'),
	('rst', 'Bachelor of Computer Science (Honours) in Interactive Software Technology'),
	('rsw', 'Bachelor of Software Engineering (Honours)');

-- Dumping structure for table focs-website.SPMholder
DROP TABLE IF EXISTS `SPMholder`;
CREATE TABLE IF NOT EXISTS `SPMholder` (
  `Name` varchar(50) NOT NULL,
  `IcNo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.SPMholder: ~1 rows (approximately)
INSERT INTO `SPMholder` (`Name`, `IcNo`) VALUES
	('Tan Kang Hong', '111111-11-1111');

-- Dumping structure for table focs-website.staff
DROP TABLE IF EXISTS `staff`;
CREATE TABLE IF NOT EXISTS `staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_name` varchar(150) DEFAULT NULL,
  `avatar` varchar(50) DEFAULT NULL,
  `designation` varchar(50) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  KEY `staff_name_idx` (`staff_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.staff: ~10 rows (approximately)
INSERT INTO `staff` (`staff_id`, `staff_name`, `avatar`, `designation`, `department`, `position`, `email`) VALUES
	(1, 'Dr. Lim Wei Jie', 'staff_m.png', 'Dean', 'Faculty of Computing And Information Technology', 'Senior Lecturer', 'limwj@tarc.edu.my'),
	(2, 'Prof. Nurul Aida', 'staff_f.png', 'Deputy Dean', 'Faculty of Computing And Information Technology', 'Principal Lecturer', 'nurula@tarc.edu.my'),
	(3, 'Mr. Mohd Shaharuddin', 'staff_m.png', 'Associate Dean', 'Department of Software Engineering And Technology', 'Senior Lecturer', 'mohds@tarc.edu.my'),
	(4, 'Dr. Siti Amanah', 'staff_f.png', 'Programme Leader', 'Department of Software Engineering And Technology', 'Lecturer', 'sitia@tarc.edu.my'),
	(5, 'Mr. Cheng Cai Jie', 'staff_m.png', 'Programme Leader', 'Department of Software Engineering And Technology', 'Senior Lecturer', 'chengcj@tarc.edu.my'),
	(6, 'Prof. Tan Kan Hong', 'staff_m.png', NULL, 'Department of Software Engineering And Technology', 'Assistant Professor', 'tankh@tarc.edu.my'),
	(7, 'Dr. Muhammad Azlan', 'staff_m.png', NULL, 'Department of Software Engineering And Technology', 'Lecturer', 'muhammada@tarc.edu.my'),
	(8, 'Ms. Norliza Ismail', 'staff_f.png', 'Associate Dean', 'Department of Mathematical And Data Science', 'Principal Lecturer', 'norlizai@tarc.edu.my'),
	(9, 'Prof. Ahmad Firdaus', 'staff_m.png', 'Programme Leader', 'Department of Mathematical And Data Science', 'Senior Lecturer', 'ahmada@tarc.edu.my'),
	(10, 'Dr. Tan Mei Ling', 'staff_f.png', 'Course Leader', 'Department of Mathematical And Data Science', 'Assistant Professor', 'tanml@tarc.edu.my');

-- Dumping structure for table focs-website.staff_details
DROP TABLE IF EXISTS `staff_details`;
CREATE TABLE IF NOT EXISTS `staff_details` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `publications` text DEFAULT NULL,
  `specialization` text DEFAULT NULL,
  `area_of_interest` text DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  CONSTRAINT `FK__staff` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.staff_details: ~1 rows (approximately)
INSERT INTO `staff_details` (`staff_id`, `publications`, `specialization`, `area_of_interest`) VALUES
	(1, 'eeee', 'Management Information Systems', '*Information Security<br>*Networking');

-- Dumping structure for table focs-website.subject
DROP TABLE IF EXISTS `subject`;
CREATE TABLE IF NOT EXISTS `subject` (
  `value` varchar(50) NOT NULL,
  `programme_id` int(11) NOT NULL,
  `elective_idx` tinyint(4) NOT NULL DEFAULT -1,
  PRIMARY KEY (`value`,`programme_id`),
  KEY `FK_subject_programme` (`programme_id`),
  CONSTRAINT `FK_subject_programme` FOREIGN KEY (`programme_id`) REFERENCES `programme` (`programme_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;

-- Dumping data for table focs-website.subject: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
