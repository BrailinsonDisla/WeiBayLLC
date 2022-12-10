DROP DATABASE WeiBayLLC;
CREATE DATABASE IF NOT EXISTS WeiBayLLC;
USE WeiBayLLC;

CREATE TABLE RegisteredUsers (
    `User ID`       INT UNIQUE AUTO_INCREMENT,

    `First Name`    VARCHAR(45) NOT NULL,
    `Last Name`     VARCHAR(45) NOT NULL,

    `Username`      VARCHAR(45) NOT NULL,
    `Email`         VARCHAR(45) NOT NULL,
    `Password`       VARCHAR(255) NOT NULL,
    `Role`          CHAR(5) DEFAULT 'RUSER',

    `Phone`         CHAR(12) DEFAULT NULL,
    `Address`       INT DEFAULT NULL,
    `Bank Account`  INT DEFAULT NULL,

    PRIMARY KEY (`User ID`),
    UNIQUE (`Email`),

    CHECK (Role IN ('ADMIN', 'RUSER')),
    CHECK (Phone LIKE '___-___-___')
);

CREATE TABLE PendingApprovalUsers (
    `User ID`       INT UNIQUE AUTO_INCREMENT,

    `First Name`    VARCHAR(45) NOT NULL,
    `Last Name`     VARCHAR(45) NOT NULL,

    `Username`      VARCHAR(45) NOT NULL,
    `Email`         VARCHAR(45) NOT NULL,
    `Password`       VARCHAR(255) NOT NULL,
    `Role`          CHAR(5) DEFAULT 'RUSER',

    `Phone`         CHAR(12) DEFAULT NULL,
    `Address`       INT DEFAULT NULL,
    `Bank Account`  INT DEFAULT NULL,

    PRIMARY KEY (`User ID`),
    UNIQUE (`Email`),

    CHECK (Role IN ('ADMIN', 'RUSER')),
    CHECK (Phone LIKE '___-___-___')
);

CREATE TABLE DeniedUsers (
    `User ID`       INT UNIQUE AUTO_INCREMENT,

    `First Name`    VARCHAR(45) NOT NULL,
    `Last Name`     VARCHAR(45) NOT NULL,

    `Username`      VARCHAR(45) NOT NULL,
    `Email`         VARCHAR(45) NOT NULL,
    `Password`       VARCHAR(255) NOT NULL,
    `Role`          CHAR(5) DEFAULT 'RUSER',

    `Phone`         CHAR(12) DEFAULT NULL,
    `Address`       INT DEFAULT NULL,
    `Bank Account`  INT DEFAULT NULL,

    PRIMARY KEY (`User ID`),
    UNIQUE (`Email`),

    CHECK (Role IN ('ADMIN', 'RUSER')),
    CHECK (Phone LIKE '___-___-___')
);

CREATE TABLE BannedUsers (
    `User ID`       INT UNIQUE AUTO_INCREMENT,

    `First Name`    VARCHAR(45) NOT NULL,
    `Last Name`     VARCHAR(45) NOT NULL,

    `Username`      VARCHAR(45) NOT NULL,
    `Email`         VARCHAR(45) NOT NULL,
    `Password`       VARCHAR(255) NOT NULL,
    `Role`          CHAR(5) DEFAULT 'RUSER',

    `Phone`         CHAR(12) DEFAULT NULL,
    `Address`       INT DEFAULT NULL,
    `Bank Account`  INT DEFAULT NULL,

    PRIMARY KEY (`User ID`),
    UNIQUE (`Email`),

    CHECK (Role IN ('ADMIN', 'RUSER')),
    CHECK (Phone LIKE '___-___-___')
);

CREATE TABLE Addresses (
    `Address ID`    INT UNIQUE AUTO_INCREMENT,

    `Address`       VARCHAR(45) NOT NULL,
    `City`          VARCHAR(45) NOT NULL,
    `State`         VARCHAR(45) NOT NULL,
    `Postal`        INT NOT NULL,
    `Country`       VARCHAR(45) NOT NULL
);

CREATE TABLE BankAccounts (
    `Account Number`    INT UNIQUE AUTO_INCREMENT,

    `Owner`             INT DEFAULT NULL,
    `Account Balance`   INT NOT NULL DEFAULT 1000.0,

    PRIMARY KEY (`Account Number`)
);

ALTER TABLE RegisteredUsers ADD CONSTRAINT AddressRUFK
    FOREIGN KEY (`Address`) REFERENCES Addresses (`Address ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

ALTER TABLE RegisteredUsers ADD CONSTRAINT BankAccountRUFK
    FOREIGN KEY (`Bank Account`) REFERENCES BankAccounts (`Account Number`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

ALTER TABLE PendingApprovalUsers ADD CONSTRAINT AddressPRUFK
    FOREIGN KEY (`Address`) REFERENCES Addresses (`Address ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

ALTER TABLE PendingApprovalUsers ADD CONSTRAINT BankAccountPRUFK
    FOREIGN KEY (`Bank Account`) REFERENCES BankAccounts (`Account Number`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

ALTER TABLE DeniedUsers ADD CONSTRAINT AddressDUFK
    FOREIGN KEY (`Address`) REFERENCES Addresses (`Address ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

ALTER TABLE DeniedUsers ADD CONSTRAINT BankAccountDUFK
    FOREIGN KEY (`Bank Account`) REFERENCES BankAccounts (`Account Number`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

ALTER TABLE BannedUsers ADD CONSTRAINT AddressBUFK
    FOREIGN KEY (`Address`) REFERENCES Addresses (`Address ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

ALTER TABLE BannedUsers ADD CONSTRAINT BankAccountBUFK
    FOREIGN KEY (`Bank Account`) REFERENCES BankAccounts (`Account Number`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

ALTER TABLE BankAccounts ADD CONSTRAINT OwnerFK
    FOREIGN KEY (`Owner`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL;

CREATE TABLE ListedProducts (
    `Product ID`    INT UNIQUE AUTO_INCREMENT,
    `Seller`        INT NOT NULL,

    `Product Name`  VARCHAR(255) NOT NULL,
    `Description`   VARCHAR(1024) NOT NULL,

    `Condition`     VARCHAR(4) NOT NULL DEFAULT 'NEW',
    `Quantity`      INT NOT NULL DEFAULT 1,
    `Price`         INT NOT NULL,
    `Rating`        FLOAT,

    PRIMARY KEY (`Product ID`),

    FOREIGN KEY (`Seller`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,

    CHECK (`Condition` IN ('NEW', 'USED')),
    CHECK (Rating BETWEEN 0 AND 5)
);

CREATE TABLE PendingApprovalProducts (
    `Product ID`    INT UNIQUE AUTO_INCREMENT,
    `Seller`        INT NOT NULL,

    `Product Name`  VARCHAR(255) NOT NULL,
    `Description`   VARCHAR(1024) NOT NULL,

    `Condition`     VARCHAR(4) NOT NULL DEFAULT 'NEW',
    `Quantity`      INT NOT NULL DEFAULT 1,
    `Price`         INT NOT NULL,
    `Rating`        FLOAT,

    PRIMARY KEY (`Product ID`),
    FOREIGN KEY (`Seller`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,

    CHECK (`Condition` IN ('NEW', 'USED')),
    CHECK (Rating BETWEEN 0 AND 5)
);

CREATE TABLE DeniedProducts (
    `Product ID`    INT UNIQUE AUTO_INCREMENT,
    `Seller`        INT NOT NULL,

    `Product Name`  VARCHAR(255) NOT NULL,
    `Description`   VARCHAR(1024) NOT NULL,

    `Condition`     VARCHAR(4) NOT NULL DEFAULT 'NEW',
    `Quantity`      INT NOT NULL DEFAULT 1,
    `Price`         INT NOT NULL,
    `Rating`        FLOAT,

    PRIMARY KEY (`Product ID`),
    FOREIGN KEY (`Seller`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,

    CHECK (`Condition` IN ('NEW', 'USED')),
    CHECK (Rating BETWEEN 0 AND 5)
);

CREATE TABLE BannedProducts (
    `Product ID`    INT UNIQUE AUTO_INCREMENT,
    `Seller`        INT DEFAULT NULL,

    `Product Name`  VARCHAR(255) NOT NULL,
    `Description`   VARCHAR(1024) NOT NULL,

    `Condition`     VARCHAR(4) NOT NULL DEFAULT 'NEW',
    `Quantity`      INT NOT NULL DEFAULT 1,
    `Price`         INT NOT NULL,
    `Rating`        FLOAT,

    PRIMARY KEY (`Product ID`),
    FOREIGN KEY (`Seller`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL,

    CHECK (`Condition` IN ('NEW', 'USED')),
    CHECK (Rating BETWEEN 0 AND 5)
);

CREATE TABLE PendingApprovalReports (
    `Report ID`     INT UNIQUE AUTO_INCREMENT,
#     `Posting ID`    INT NOT NULL,
    `Product ID`    INT,
    `Seller ID`     INT,
    `Reporter ID`   INT,
    `Reason`        VARCHAR(2096),

    PRIMARY KEY (`Report ID`),

#     FOREIGN KEY (`Posting ID`) REFERENCES Postings(`Posting ID`)
#                             ON UPDATE CASCADE
#                             ON DELETE CASCADE,
    FOREIGN KEY (`Product ID`) REFERENCES ListedProducts(`Product ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL,
    FOREIGN KEY (`Seller ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL,
    FOREIGN KEY (`Reporter ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL
);

CREATE TABLE ApprovedReports (
    `Report ID`     INT UNIQUE AUTO_INCREMENT,
#     `Posting ID`    INT NOT NULL,
    `Product ID`    INT,
    `Seller ID`     INT,
    `Reporter ID`   INT,
    `Reason`        VARCHAR(2096),

    PRIMARY KEY (`Report ID`),

#     FOREIGN KEY (`Posting ID`) REFERENCES Postings(`Posting ID`)
#                             ON UPDATE CASCADE
#                             ON DELETE CASCADE,
    FOREIGN KEY (`Product ID`) REFERENCES ListedProducts(`Product ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL,
    FOREIGN KEY (`Seller ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL,
    FOREIGN KEY (`Reporter ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL
);

CREATE TABLE DeniedReports (
    `Report ID`     INT UNIQUE AUTO_INCREMENT,
#     `Posting ID`    INT NOT NULL,
    `Product ID`    INT,
    `Seller ID`     INT,
    `Reporter ID`   INT,
    `Reason`        VARCHAR(2096),

    PRIMARY KEY (`Report ID`),

#     FOREIGN KEY (`Posting ID`) REFERENCES Postings(`Posting ID`)
#                             ON UPDATE CASCADE
#                             ON DELETE CASCADE,
    FOREIGN KEY (`Product ID`) REFERENCES ListedProducts(`Product ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL,
    FOREIGN KEY (`Seller ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL,
    FOREIGN KEY (`Reporter ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL
);

CREATE TABLE Orders (
    `Order ID`            INT UNIQUE AUTO_INCREMENT,
    `Buyer ID`            INT NOT NULL,
    `Total`               FLOAT NOT NULL,
    `Order Date`          DATETIME NOT NULL,
    `Shipping Address`    INT,

    PRIMARY KEY (`Order ID`),

    FOREIGN KEY (`Buyer ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,
    FOREIGN KEY (`Shipping Address`) REFERENCES Addresses(`Address ID`)
                            ON UPDATE CASCADE
                            ON DELETE SET NULL
);

CREATE TABLE SavedProducts (
    `SP ID`         INT UNIQUE NOT NULL,
    `Product ID`    INT NOT NULL,
    `User ID`       INT NOT NULL,

    PRIMARY KEY (`SP ID`),

    FOREIGN KEY (`Product ID`) REFERENCES ListedProducts(`Product ID`)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,
    FOREIGN KEY (`User ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE
);

CREATE TABLE Bids (
    `Bid ID`        INT UNIQUE NOT NULL,
    `Product ID`    INT NOT NULL,
    `User ID`       INT NOT NULL,
    `Bid`           FLOAT NOT NULL,

    PRIMARY KEY (`Bid ID`),

    FOREIGN KEY (`Product ID`) REFERENCES ListedProducts(`Product ID`)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE,
    FOREIGN KEY (`User ID`) REFERENCES RegisteredUsers(`User ID`)
                            ON UPDATE CASCADE
                            ON DELETE CASCADE

);