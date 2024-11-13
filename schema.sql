CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT
);
CREATE TABLE groups (id SERIAL PRIMARY KEY);
CREATE TABLE userGroups (
    userId INT REFERENCES users(id) ON DELETE CASCADE,
    groupId INT REFERENCES groups(id) ON DELETE CASCADE,
    PRIMARY KEY (userId, groupId),
    role INT,
    UNIQUE (userId)
);
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    companyName TEXT NOT NULL,
    businessId TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    websiteUrl TEXT DEFAULT '',
    email TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    address TEXT DEFAULT '',
    groupId INT NOT NULL,
    FOREIGN KEY (groupId) REFERENCES groups(id) ON DELETE CASCADE
);
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    firstName TEXT NOT NULL,
    lastName TEXT,
    email TEXT,
    phone TEXT,
    companyId INT NOT NULL,
    FOREIGN KEY (companyId) REFERENCES companies(id) ON DELETE CASCADE
);