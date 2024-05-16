create table online_ordering_system.db_user_roles
(
    user_id int not null,
    role_id int not null,
    primary key (user_id, role_id),
    constraint db_user_roles_ibfk_1
        foreign key (role_id) references online_ordering_system.tb_role (id),
    constraint db_user_roles_ibfk_2
        foreign key (user_id) references online_ordering_system.tb_user (id)
);

create index role_id
    on online_ordering_system.db_user_roles (role_id);

