create table online_ordering_system.db_order_foods
(
    order_id int not null,
    food_id  int not null,
    quality  int null,
    primary key (order_id, food_id),
    constraint db_order_foods_ibfk_1
        foreign key (food_id) references online_ordering_system.tb_food (id),
    constraint db_order_foods_ibfk_2
        foreign key (order_id) references online_ordering_system.tb_order (id)
);

create index food_id
    on online_ordering_system.db_order_foods (food_id);

