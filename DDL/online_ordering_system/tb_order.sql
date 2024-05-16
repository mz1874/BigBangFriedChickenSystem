create table online_ordering_system.tb_order
(
    id         int auto_increment
        primary key,
    order_time datetime null,
    total      float    not null,
    status     int      not null,
    user_id    int      not null,
    constraint tb_order_ibfk_1
        foreign key (user_id) references online_ordering_system.tb_user (id)
);

create index user_id
    on online_ordering_system.tb_order (user_id);

