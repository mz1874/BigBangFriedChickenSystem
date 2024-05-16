create table online_ordering_system.tb_feedback
(
    id         int auto_increment
        primary key,
    name       varchar(60)  not null,
    email      varchar(60)  not null,
    category   varchar(60)  not null,
    visit_type varchar(60)  not null,
    time_visit varchar(60)  not null,
    date_visit varchar(20)  not null,
    subject    varchar(60)  not null,
    message    varchar(255) not null
);

