create table online_ordering_system.tb_food
(
    id          int auto_increment
        primary key,
    food_name   varchar(50)  not null,
    price       float        null,
    img         varchar(100) not null,
    category_id int          not null,
    constraint food_name
        unique (food_name),
    constraint img
        unique (img),
    constraint tb_food_ibfk_1
        foreign key (category_id) references online_ordering_system.tb_category (id)
);

create index category_id
    on online_ordering_system.tb_food (category_id);

