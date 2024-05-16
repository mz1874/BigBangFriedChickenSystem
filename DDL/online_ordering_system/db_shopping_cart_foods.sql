create table online_ordering_system.db_shopping_cart_foods
(
    shopping_cart_id int      not null,
    food_id          int      not null,
    created_at       datetime null,
    quality          int      null,
    primary key (shopping_cart_id, food_id),
    constraint db_shopping_cart_foods_ibfk_1
        foreign key (food_id) references online_ordering_system.tb_food (id),
    constraint db_shopping_cart_foods_ibfk_2
        foreign key (shopping_cart_id) references online_ordering_system.tb_shopping_cart (id)
);

create index food_id
    on online_ordering_system.db_shopping_cart_foods (food_id);

