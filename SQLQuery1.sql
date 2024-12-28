CREATE TABLE Users (
	UniqueID NVARCHAR(20) PRIMARY KEY,
    UserID INT,
    FullName NVARCHAR(100),
    Email NVARCHAR(100),
    MobileNo NVARCHAR(20),
    Passwords NVARCHAR(100),
    DoB DATE,
    Category NVARCHAR(50)
);

CREATE TABLE Results (
    UniqueID NVARCHAR(20) PRIMARY KEY,
    Category VARCHAR(50),
    mocktest1 INT,
    mocktest2 INT,
    mocktest3 INT,
    mocktest4 INT,
    mocktest5 INT,
    mocktest6 INT,
    mocktest7 INT,
    mocktest8 INT,
    mocktest9 INT,
    mocktest10 INT,
    NeetFinalScore INT,
	FOREIGN KEY (UniqueID) REFERENCES Users(UniqueID)
);

CREATE TABLE Admins (
    Username VARCHAR(50) PRIMARY KEY,
    Passwords VARCHAR(50) NOT NULL
);

INSERT INTO Admins (Username, Passwords) VALUES ('admin', 'admin_password');

SELECT Email, MobileNo, UniqueID, Category FROM Users;

USE NeetRegistration

CREATE TABLE Responses (
    UniqueID INT,
    QuestionNumber INT,
    Response VARCHAR(255)
);

CREATE TABLE UserMockTests (
    UniqueID NVARCHAR(20),
    MockTestNumber INT,
    Completed BIT,
    CONSTRAINT PK_UserMockTests PRIMARY KEY (UniqueID, MockTestNumber),
    CONSTRAINT FK_UserMockTests_UserID FOREIGN KEY (UniqueID) REFERENCES Users(UniqueID),
    CONSTRAINT CK_MockTestNumber CHECK (MockTestNumber BETWEEN 1 AND 10)
);

