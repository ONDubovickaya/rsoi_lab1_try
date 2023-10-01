CREATE TABLE if not exists Persons (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL,
    age integer,
    address varchar(50),
    work varchar(50)
);
