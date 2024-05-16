create table online_ordering_system.tb_category
(
    id            int auto_increment
        primary key,
    category_name varchar(50) not null,
    constraint category_name
        unique (category_name)
);

