CREATE TABLE IF NOT EXISTS pages (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(id),
    contents MEDIUMTEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS password (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(id),
    password TEXT NOT NULL
);

ALTER TABLE pages ADD title VARCHAR(1024);
