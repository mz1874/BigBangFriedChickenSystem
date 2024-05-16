create table online_ordering_system.db_user_order
(
    user_id  int not null,
    order_id int not null,
    primary key (user_id, order_id),
    constraint db_user_order_ibfk_1
        foreign key (order_id) references online_ordering_system.tb_order (id),
    constraint db_user_order_ibfk_2
        foreign key (user_id) references online_ordering_system.tb_user (id)
);

create index order_id
    on online_ordering_system.db_user_order (order_id);

