create table online_ordering_system.tb_shopping_cart
(
    id      int auto_increment
        primary key,
    user_id int not null,
    constraint tb_shopping_cart_ibfk_1
        foreign key (user_id) references online_ordering_system.tb_user (id)
);

create index user_id
    on online_ordering_system.tb_shopping_cart (user_id);

