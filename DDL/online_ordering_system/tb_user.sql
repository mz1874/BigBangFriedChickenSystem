create table online_ordering_system.tb_user
(
    id       int auto_increment
        primary key,
    username varchar(50)  not null,
    password varchar(100) not null,
    sex      tinyint(1)   null,
    address  varchar(100) not null,
    constraint username
        unique (username)
);

