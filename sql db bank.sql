-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema bank_delivery2
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `bank_delivery2` ;

-- -----------------------------------------------------
-- Schema bank_delivery2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bank_delivery2` DEFAULT CHARACTER SET utf8mb4;
USE `bank_delivery2` ;

-- -----------------------------------------------------
-- Table `bank_delivery2`.`customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_delivery2`.`customer` ;

CREATE TABLE IF NOT EXISTS `bank_delivery2`.`customer` (
  `customerID` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `age` SMALLINT UNSIGNED NOT NULL,
  `CPR` VARCHAR(12) NOT NULL,
  `addres` VARCHAR(255) NOT NULL,
  `postcode` VARCHAR(10) NULL DEFAULT NULL,
  `City` VARCHAR(55) NOT NULL,
  `Country` VARCHAR(45) NOT NULL,
  `ID_photo_front` VARBINARY(8000) NULL DEFAULT NULL,
  `ID_photo_back` VARBINARY(8000) NULL DEFAULT NULL,
  `Gender` ENUM('M', 'F', 'O') NOT NULL,
  `phonenumber` BIGINT NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `datecreated` DATETIME NOT NULL,
  PRIMARY KEY (`customerID`),
  UNIQUE INDEX `customerID_UNIQUE` (`customerID` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bank_delivery2`.`accounts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_delivery2`.`accounts` ;

CREATE TABLE IF NOT EXISTS `bank_delivery2`.`accounts` (
  `account_number` VARCHAR(55) NOT NULL,
  `customerID` INT NOT NULL AUTO_INCREMENT,
  `Balance` DOUBLE(255,2) NOT NULL DEFAULT '0.00',
  `Card_number` BIGINT NOT NULL,
  `Expire_date` VARCHAR(5) NOT NULL,
  `CVC` INT NOT NULL,
  `Currency` VARCHAR(55) NOT NULL,
  `PaymentCardType` ENUM('VISA', 'MASTERCARD', 'MAESTRO') NOT NULL,
  `CardType` ENUM('Debit', 'Credit') NOT NULL,
  `AccountType` ENUM('Personal', 'Business') NOT NULL,
  `CardStatus` TINYINT(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`account_number`),
  INDEX `customerID` (`customerID` ASC) VISIBLE,
  UNIQUE INDEX `account_number_UNIQUE` (`account_number` ASC) VISIBLE,
  UNIQUE INDEX `Card_number_UNIQUE` (`Card_number` ASC) VISIBLE,
  CONSTRAINT `accounts_ibfk_1`
    FOREIGN KEY (`customerID`)
    REFERENCES `bank_delivery2`.`customer` (`customerID`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bank_delivery2`.`customer_profile`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_delivery2`.`customer_profile` ;

CREATE TABLE IF NOT EXISTS `bank_delivery2`.`customer_profile` (
  `CustomerID` INT NOT NULL AUTO_INCREMENT,
  `CustomerIncome` DOUBLE(255,2) NULL DEFAULT NULL,
  `CustomerCreditScore` TINYINT NULL DEFAULT NULL,
  `CustomerSpendings` DOUBLE(255,2) NULL DEFAULT NULL,
  `CustomerSavings` DOUBLE(255,2) NULL DEFAULT NULL,
  INDEX `CustomerID` (`CustomerID` ASC) VISIBLE,
  CONSTRAINT `customer_profile_ibfk_1`
    FOREIGN KEY (`CustomerID`)
    REFERENCES `bank_delivery2`.`customer` (`customerID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bank_delivery2`.`logininformation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_delivery2`.`logininformation` ;

CREATE TABLE IF NOT EXISTS `bank_delivery2`.`logininformation` (
  `CustomerID` INT NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(55) NULL DEFAULT NULL,
  `Passwd` CHAR(64) NULL DEFAULT NULL,
  INDEX `CustomerID` (`CustomerID` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bank_delivery2`.`transactions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_delivery2`.`transactions` ;

CREATE TABLE IF NOT EXISTS `bank_delivery2`.`transactions` (
  `Transaction_ID` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `customerID` INT NOT NULL,
  `Sender_ACC_NR` VARCHAR(55) NOT NULL,
  `Receiver_ACC_NR` VARCHAR(55) NOT NULL,
  `AMOUNT` DOUBLE(255,2) NOT NULL,
  `Currency` VARCHAR(55) NOT NULL,
  `DateTime` DATETIME NOT NULL,
  INDEX `customerID` (`customerID` ASC) VISIBLE,
  INDEX `Sender_ACC_NR` (`Sender_ACC_NR` ASC) VISIBLE,
  PRIMARY KEY (`Transaction_ID`),
  CONSTRAINT `transcation_history_ibfk_1`
    FOREIGN KEY (`customerID`)
    REFERENCES `bank_delivery2`.`customer` (`customerID`),
  CONSTRAINT `transcation_history_ibfk_2`
    FOREIGN KEY (`Sender_ACC_NR`)
    REFERENCES `bank_delivery2`.`accounts` (`account_number`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `bank_delivery2`.`ATM`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_delivery2`.`ATM` ;

CREATE TABLE IF NOT EXISTS `bank_delivery2`.`ATM` (
  `atmID` INT NOT NULL,
  `ATM_Name` VARCHAR(45) NOT NULL,
  `Location_addres` VARCHAR(55) NOT NULL,
  `City` VARCHAR(45) NOT NULL,
  `Country` VARCHAR(45) NOT NULL,
  `Total_Balance` INT NOT NULL,
  `100bills` INT NULL,
  `200bills` INT NULL DEFAULT 0,
  `500bills` INT NULL DEFAULT 0,
  `1000bills` INT NULL DEFAULT 0,
  PRIMARY KEY (`atmID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
CREATE TABLE `bank_delivery2`.`crypto_assets` (
  `cryptoID` INT NOT NULL AUTO_INCREMENT,
  `crypto_name` VARCHAR(45) NOT NULL,
  `Crypto_current_price` DOUBLE(255,2) NULL,
  `Crypto_abv` VARCHAR(45) NULL,
  `Crypto_max_52` DOUBLE(255,2) NULL,
  `Crypto_min_52` DOUBLE(255,2) NULL,
  PRIMARY KEY (`cryptoID`));

CREATE TABLE `bank_delivery2`.`crypto_trades` (
  `tradeID` INT NOT NULL AUTO_INCREMENT,
  `customerID` INT NOT NULL,
  `cryptoID` INT NOT NULL,
  `trade_open` DOUBLE(255,2) NOT NULL,
  `trade_close` DOUBLE(255,2) NULL,
  `trade_value` VARCHAR(45) NOT NULL,
  `trade_units` DOUBLE(255,2) NOT NULL,
  `trade_open_date` DATETIME NOT NULL,
  `trade_close_date` DATETIME NULL,
  `trade_active` TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`tradeID`),
  INDEX `cryptoID_idx` (`cryptoID` ASC) VISIBLE,
  INDEX `customerID_idx` (`customerID` ASC) VISIBLE,
  CONSTRAINT `cryptoID`
    FOREIGN KEY (`cryptoID`)
    REFERENCES `bank_delivery2`.`crypto_assets` (`cryptoID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `customerID`
    FOREIGN KEY (`customerID`)
    REFERENCES `bank_delivery2`.`customer` (`customerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
    
    
CREATE TABLE `bank_delivery2`.`customer_trading_account` (
  `trading_accountID` INT NOT NULL AUTO_INCREMENT,
  `customerID` INT NOT NULL,
  `available_balance` DOUBLE(255,2) NOT NULL DEFAULT 0,
  `equity` DOUBLE(255,2) NULL DEFAULT 0,
  `total_tax` DOUBLE(255,2) NULL DEFAULT 0,
  PRIMARY KEY (`trading_accountID`),
  INDEX `customerID_idx` (`customerID` ASC) VISIBLE,
  CONSTRAINT `tradingcustomerID`
    FOREIGN KEY (`customerID`)
    REFERENCES `bank_delivery2`.`customer` (`customerID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


ALTER TABLE `bank_delivery2`.`accounts` 
ADD COLUMN `International_transfers` TINYINT(1) NOT NULL DEFAULT 0 AFTER `CardStatus`,
ADD COLUMN `International_atm_withdrawals` TINYINT(1) NOT NULL DEFAULT 0 AFTER `International_transfers`;


ALTER TABLE bank_delivery2.customer AUTO_INCREMENT = 1;
ALTER TABLE bank_delivery2.accounts AUTO_INCREMENT = 1;
ALTER TABLE bank_delivery2.logininformation AUTO_INCREMENT = 1;

ALTER TABLE `bank_delivery2`.`crypto_trades` 
CHANGE COLUMN `trade_value` `trade_value` VARCHAR(45) NULL ;

ALTER TABLE `bank_delivery2`.`logininformation` 
CHANGE COLUMN `Passwd` `Passwd` VARCHAR(256) NULL DEFAULT NULL ;


INSERT INTO crypto_assets (crypto_name, Crypto_abv)
VALUES ('BITCOIN', 'BTC');

INSERT INTO crypto_assets (crypto_name, Crypto_abv, Crypto_current_price)
VALUES ('Etherium', 'ETH', 15000);

INSERT INTO crypto_assets (crypto_name, Crypto_abv, Crypto_current_price)
VALUES ('Dogecoin', 'DOGE', 1.99);

ALTER TABLE `bank_delivery2`.`crypto_trades` 
DROP FOREIGN KEY `customerID`;
ALTER TABLE `bank_delivery2`.`crypto_trades` 
DROP COLUMN `trade_active`,
DROP INDEX `customerID_idx` ;
;

ALTER TABLE `bank_delivery2`.`customer_trading_account` 
ADD COLUMN `first_name` VARCHAR(45) NOT NULL AFTER `customerID`,
ADD COLUMN `last_name` VARCHAR(45) NOT NULL AFTER `first_name`;

ALTER TABLE `bank_delivery2`.`customer_trading_account` 
DROP FOREIGN KEY `tradingcustomerID`;
ALTER TABLE `bank_delivery2`.`customer_trading_account` 
DROP COLUMN `trading_accountID`,
CHANGE COLUMN `customerID` `customerID` INT NOT NULL AUTO_INCREMENT ,
ADD INDEX `customertradeID_idx` (`customerID` ASC) VISIBLE,
DROP INDEX `customerID_idx` ,
DROP PRIMARY KEY;
;
ALTER TABLE `bank_delivery2`.`customer_trading_account` 
ADD CONSTRAINT `customertradeID`
  FOREIGN KEY (`customerID`)
  REFERENCES `bank_delivery2`.`customer` (`customerID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

