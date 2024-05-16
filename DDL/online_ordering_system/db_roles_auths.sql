create table online_ordering_system.db_roles_auths
(
    role_id int not null,
    auth_id int not null,
    primary key (role_id, auth_id),
    constraint db_roles_auths_ibfk_1
        foreign key (auth_id) references online_ordering_system.tb_authorization (id),
    constraint db_roles_auths_ibfk_2
        foreign key (role_id) references online_ordering_system.tb_role (id)
);

create index auth_id
    on online_ordering_system.db_roles_auths (auth_id);

