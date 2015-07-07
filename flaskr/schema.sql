drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  name_id text not null,
  mail_id text not null,
  amount integer not null
);