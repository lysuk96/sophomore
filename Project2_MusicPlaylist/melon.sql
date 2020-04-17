/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

DROP DATABASE IF EXISTS `melon`;
CREATE DATABASE IF NOT EXISTS `melon` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `melon`;

DROP TABLE IF EXISTS `administrator`;
CREATE TABLE IF NOT EXISTS `administrator` (
	Id	CHAR(5)	NOT NULL,
	`Name`	VARCHAR(20) NOT NULL,
	Sex	CHAR(1)	DEFAULT NULL,
	Address	VARCHAR(30) DEFAULT NULL,
	Phone_no	VARCHAR(13)	DEFAULT NULL,
	Mgr_id	CHAR(5) DEFAULT NULL,
	PRIMARY KEY (Id),
	KEY Mgr_id (Mgr_id),
	CONSTRAINT administrator_ibfk_1 FOREIGN KEY (Mgr_id) REFERENCES administrator (id)
	ON DELETE SET NULL	ON UPDATE CASCADE
	);

INSERT INTO `administrator` (`Name`, Id, Mgr_id, Sex, Address, Phone_no) VALUES 
('root', '11111', NULL, 'F', 'Hanyang Univ', '01011111111'),
('Paul', '12345', NULL, 'M', 'Hang Daeng', '01027596400'),
('Kevin', '01125', '11111', 'M', 'Wangsimni', '01057779888'),
('Christina', '11112', '11111', 'F', 'Han River', '01025552444'),
('Joshua', '22222', '11111', 'F', 'Gimpo', '010622222222'),
('Charlie', '33333', '12345', 'M', 'Incheon', '010422342222');

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
	Id	CHAR(5)	NOT NULL,
	`Name`	VARCHAR(15) NOT NULL,
	Sex	CHAR(1) DEFAULT NULL,
	Coin	INT(6)	DEFAULT 0,
	Address VARCHAR(30) DEFAULT NULL,
	Phone_no	VARCHAR(13) DEFAULT NULL,
	Ad_id CHAR(5)	DEFAULT NULL,
	Banned	BOOL	DEFAULT FALSE,
	PRIMARY KEY (Id),
	KEY Ad_id (Ad_id),
	CONSTRAINT user_ibfk_1 FOREIGN KEY (Ad_id) REFERENCES administrator (Id)
	ON DELETE SET NULL	ON UPDATE CASCADE
	);
INSERT INTO `user` (`name`, Id, Ad_id, Sex, Coin, Address, Phone_no) VALUES 
('Lee', '00002', '11111', 'F', 0, 'Dongdaemun', '01010101010'),
('Kim', '00001', '12345', 'M', 30, 'BackStreet', '01052225222'),
('Park', '00003', '01125', 'M', 60, 'Gwangju', '01029992999'),
('Choi', '00004', '33333', 'F', 20, 'Busan', '01058889222');

DROP TABLE IF EXISTS `playlist`;
CREATE TABLE IF NOT EXISTS `playlist` (
	Usr_id CHAR(5) NOT NULL,
	PRIMARY KEY (Usr_id),
	KEY Usr_id (Usr_id),
	CONSTRAINT playlist_ibfk_1 FOREIGN KEY (Usr_id) REFERENCES `user` (Id)
	);
INSERT INTO `playlist` (Usr_id) VALUES
('00002'), ('00001'), ('00003'), ('00004');

DROP TABLE IF EXISTS `music`;	
CREATE TABLE IF NOT EXISTS `music` (
	Id	CHAR(5)	NOT NULL,
	Title VARCHAR(30)	NOT NULL,
	Artist	VARCHAR(30)	DEFAULT NULL,
	Composer VARCHAR(30) DEFAULT NULL,
	Lyricist VARCHAR(30)	DEFAULT NULL,
	Ad_id	CHAR(5)	DEFAULT NULL,
	PRIMARY KEY (Id),
	KEY Ad_id (Ad_id),
	CONSTRAINT music_ibfk_1 FOREIGN KEY (Ad_id) REFERENCES `administrator` (Id)
	ON DELETE SET NULL	ON UPDATE CASCADE
	);

INSERT INTO `music` (Title, Id, Ad_id, Artist, Composer, Lyricist) VALUES
('Snow Flower', '15555', '12345', 'Park Hyosin', 'Noil', 'Nilo'), 
('Hello', '15556', '11111', 'Adele', 'Adele', 'Adele'),
('Snowman', '15557', '01125', 'Sia', 'Sia', 'Sia'),
('Symphony', '15558', '22222', 'Dont know', 'Mola', 'Mola'),
('Sunday Morning', '15559', '33333', 'Maroon5', 'Adam', 'Chris');

DROP TABLE IF EXISTS `add_on`;
CREATE TABLE IF NOT EXISTS `add_on` (
	Msc_id	CHAR(5)	NOT NULL,
	Usr_id	CHAR(5)	NOT NULL,
	PRIMARY KEY (Msc_id, Usr_id),
	KEY Music_id (Msc_id),
	KEY Usr_id (Usr_id),
	CONSTRAINT `add_on_ibfk_1` FOREIGN KEY (Msc_id) REFERENCES `music` (Id)
	ON DELETE CASCADE	ON UPDATE CASCADE,
	CONSTRAINT `add_on_ibfk_2`	FOREIGN KEY (Usr_id)	REFERENCES	`user` (Id)
	ON DELETE CASCADE	ON UPDATE CASCADE
	);

INSERT INTO `add_on` (Msc_id, Usr_id) VALUES
('15555', '00001'),
('15555', '00002'),
('15556', '00001'),
('15556', '00002'),
('15556', '00003'),
('15557', '00001'),
('15558', '00001'),
('15559', '00001');
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;