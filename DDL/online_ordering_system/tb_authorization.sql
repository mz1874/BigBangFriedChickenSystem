create table online_ordering_system.tb_authorization
(
    id            int auto_increment
        primary key,
    auth_name     varchar(50)  not null,
    resource_path varchar(100) not null
);

