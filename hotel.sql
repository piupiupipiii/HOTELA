-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for hotel
CREATE DATABASE IF NOT EXISTS `hotel` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hotel`;

-- Dumping structure for table hotel.booking
CREATE TABLE IF NOT EXISTS `booking` (
  `id_booking` int NOT NULL AUTO_INCREMENT,
  `check_in` date DEFAULT NULL,
  `check_out` date DEFAULT NULL,
  `cara_bayar` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `total_pembelian` int DEFAULT NULL,
  `nama` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `telp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `id_tamu` int DEFAULT NULL,
  `id_rooms` int DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id_booking`),
  KEY `FK_booking_tamu` (`id_tamu`),
  KEY `FK_booking_users` (`id_user`),
  KEY `FK_booking_rooms` (`id_rooms`),
  CONSTRAINT `FK_booking_rooms` FOREIGN KEY (`id_rooms`) REFERENCES `rooms` (`id_rooms`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_booking_tamu` FOREIGN KEY (`id_tamu`) REFERENCES `tamu` (`id_tamu`),
  CONSTRAINT `FK_booking_users` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table hotel.booking: ~6 rows (approximately)
INSERT INTO `booking` (`id_booking`, `check_in`, `check_out`, `cara_bayar`, `total_pembelian`, `nama`, `telp`, `id_tamu`, `id_rooms`, `id_user`) VALUES
	(123, '2023-12-12', '2023-12-14', 'm-banking', 1400000, 'sel', '098786766', 12, 401, 3),
	(125, '2023-12-14', '2023-12-16', 'cash', 770000, 'Pipi', '0876543456', 13, 401, 4),
	(126, '2023-12-12', '2023-12-14', 'cash', 1100000, 'Pipi', '0876547', 14, 301, 4),
	(128, '2023-12-12', '2023-12-14', 'cash', 1540000, 'pipi', '09876554', 15, 702, 6),
	(129, '2023-12-11', '2023-12-13', 'cash', 1320000, 'maamh', '08765457', 16, 502, 5),
	(130, '2023-12-12', '2023-12-14', 'cash', 2000000, 'silvy', '087777', 17, 801, 9);

-- Dumping structure for table hotel.logad
CREATE TABLE IF NOT EXISTS `logad` (
  `id_logad` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `role` enum('admin') DEFAULT NULL,
  PRIMARY KEY (`id_logad`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table hotel.logad: ~1 rows (approximately)
INSERT INTO `logad` (`id_logad`, `username`, `password`, `role`) VALUES
	(1, 'pipi', 'silvy', 'admin');

-- Dumping structure for table hotel.rooms
CREATE TABLE IF NOT EXISTS `rooms` (
  `id_rooms` int NOT NULL AUTO_INCREMENT,
  `type` varchar(50) DEFAULT NULL,
  `harga` int DEFAULT NULL,
  `lantai` int DEFAULT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id_rooms`)
) ENGINE=InnoDB AUTO_INCREMENT=802 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table hotel.rooms: ~8 rows (approximately)
INSERT INTO `rooms` (`id_rooms`, `type`, `harga`, `lantai`, `status`) VALUES
	(301, 'superior', 600000, 3, 'booked'),
	(401, 'deluxe', 700000, 4, 'booked'),
	(502, 'twins bed', 660000, 5, 'booked'),
	(702, 'deluxe', 770000, 7, 'booked'),
	(703, 'deluxe', 777000, 7, 'booked'),
	(704, 'deluxe', 777000, 7, 'booked'),
	(705, 'deluxe', 700000, 7, 'Avaible'),
	(801, 'suite', 1000000, 8, 'booked');

-- Dumping structure for table hotel.tamu
CREATE TABLE IF NOT EXISTS `tamu` (
  `id_tamu` int NOT NULL AUTO_INCREMENT,
  `nama_tamu` varchar(50) DEFAULT NULL,
  `telp` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_tamu`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table hotel.tamu: ~6 rows (approximately)
INSERT INTO `tamu` (`id_tamu`, `nama_tamu`, `telp`) VALUES
	(12, 'sel', '0897654134928'),
	(13, 'Pipi', '0876543456'),
	(14, 'Pipi', '0876543456'),
	(15, 'pipi', '09876554'),
	(16, 'maamh', '08765457'),
	(17, 'silvy', '087777');

-- Dumping structure for table hotel.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table hotel.users: ~10 rows (approximately)
INSERT INTO `users` (`id`, `username`, `password`) VALUES
	(1, 'ada', 'i12'),
	(2, 'silvy', 'pipi'),
	(3, 'nur', 'azkia'),
	(4, 'Pipi', 'Mauuu.123*'),
	(5, 'Mamah', 'Mamah.123*'),
	(6, 'pipi', 'Ada.123*'),
	(7, 'pipi', 'makkqnsd'),
	(8, 'pipi', 'adaaaaaaa'),
	(9, 'silvy', '12345678'),
	(10, 'harus', 'Harus.123');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
