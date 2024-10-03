Create Database Testing
Select Database Testing
-- Create UserAuthentication Table
CREATE TABLE UserAuthentication (
    UAID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Username VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    ConfirmPassword VARCHAR(255) NOT NULL,
    PhoneNo VARCHAR(15),
    Created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated_on DATETIME
);

-- Create Users Table
CREATE TABLE Users (
    UTID INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(100),
    Middle_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    Age INT,
    Country VARCHAR(100),
    City VARCHAR(100),
    Anonymous_name VARCHAR(100),
    Postal_Code VARCHAR(20),
    UAID INT,
    FOREIGN KEY (UAID) REFERENCES UserAuthentication(UAID),
    Created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated_on DATETIME
);

-- Create UserProfileImage Table
CREATE TABLE UserProfileImage (
    UPID INT AUTO_INCREMENT PRIMARY KEY,
    Real_Image VARCHAR(255),
    Hide_Image VARCHAR(255),
    UTID INT,
    FOREIGN KEY (UTID) REFERENCES Users(UTID),
    Created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated_on DATETIME
);

-- Create UserPost Table
CREATE TABLE UserPost (
    PID INT AUTO_INCREMENT PRIMARY KEY,
    UTID INT,
    S_ID INT,
    Title VARCHAR(255),
    Content TEXT,
    UPID INT,
    SentimentsScore FLOAT,
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Created_By INT,
    Updated_At DATETIME,
    Updated_By INT,
    FOREIGN KEY (UTID) REFERENCES Users(UTID),
    FOREIGN KEY (UPID) REFERENCES UserProfileImage(UPID)
);

-- Create Comment Table
CREATE TABLE Comment (
    ComID INT AUTO_INCREMENT PRIMARY KEY,
    PID INT,
    UTID INT,
    Comment_text TEXT,
    S_ID INT,
    SentimentsScore FLOAT,
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Created_by INT,
    Updated_at DATETIME,
    Updated_by INT,
    FOREIGN KEY (PID) REFERENCES UserPost(PID),
    FOREIGN KEY (UTID) REFERENCES Users(UTID)
);

-- Create Message Table
CREATE TABLE Message (
    M_ID INT AUTO_INCREMENT PRIMARY KEY,
    UTID INT,
    S_ID INT,
    CB_ID INT,
    Message_Text TEXT,
    SentimentsScore FLOAT,
    Created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    Created_By INT,
    Updated_on DATETIME,
    Updated_By INT,
    FOREIGN KEY (UTID) REFERENCES Users(UTID)
);

-- Create ChatbotResponse Table
CREATE TABLE ChatbotResponse (
    CB_ID INT AUTO_INCREMENT PRIMARY KEY,
    CB_Text TEXT,
    SentimentsScore FLOAT,
    CB_is_biased BIT,
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Created_By INT
);
