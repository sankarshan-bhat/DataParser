DROP TABLE if exists items;
DROP TABLE if exists category;
DROP TABLE if exists bids ;
DROP TABLE if exists users;
DROP TABLE if exists itemscategoryrel;


CREATE TABLE items (
    itemid INTEGER PRIMARY KEY,
    name VARCHAR(255),
    currently REAL,
    buyprice REAL,
    firstbid REAL,
    numberofbids INTEGER,
    started date,
    ends date,
    sellerid VARCHAR(255),
    description TEXT,
    FOREIGN KEY(sellerid) REFERENCES users(userid)
);

CREATE TABLE category (
    categoryid INTEGER PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE bids(
    bidid INTEGER PRIMARY KEY,
    userid VARCHAR(255),
    time VARCHAR(255),
    amount REAL,
    itemid INTEGER,
    FOREIGN KEY(userid) REFERENCES users(userid),
    FOREIGN KEY(itemid) REFERENCES items(itemid)
);

CREATE TABLE users (
    userid VARCHAR(255) PRIMARY KEY,
    rating INTEGER,
    location VARCHAR(255),
    country VARCHAR(255),
    isseller BOOLEAN,
    isbidder BOOLEAN);

CREATE TABLE itemscategoryrel (
    itemid INTEGER,
    categoryid INTEGER,
    PRIMARY KEY (itemid, categoryid),
    FOREIGN KEY(itemid) REFERENCES items(itemid),
    FOREIGN KEY(categoryid) REFERENCES category(categoryid)
);

