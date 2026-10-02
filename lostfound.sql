
create database if not exists lostfound;
use lostfound;

create table students (
    sid char(6) primary key,
    sname varchar(30) not null,
    class varchar(5),
    phone char(10)
);

create table lost_items (
    lid char(6) primary key,
    item_name varchar(30) not null,
    category varchar(15),
    description varchar(100),
    lost_date date,
    location varchar(30),
    sid char(6),
    status varchar(10) default 'Open',
    foreign key (sid) references students(sid)
);

create table found_items (
    fid char(6) primary key,
    item_name varchar(30) not null,
    category varchar(15),
    description varchar(100),
    found_date date,
    location varchar(30),
    finder_sid char(6),
    status varchar(10) default 'Unclaimed',
    foreign key (finder_sid) references students(sid)
);

-- Sample data 
insert into students values ('S00001', 'Aarav Sharma', 'XII-A', '9000000001');
insert into students values ('S00002', 'Diya Verma', 'XI-B', '9000000002');
insert into students values ('S00003', 'Kabir Singh', 'XII-B', '9000000003');
insert into students values ('S00004', 'Meera Nair', 'X-A', '9000000004');

insert into lost_items values ('L00001', 'Water Bottle', 'Bottle', 'Blue steel bottle', '2026-09-28', 'Canteen', 'S00001', 'Open');
insert into lost_items values ('L00002', 'Geometry Box', 'Stationery', 'Camlin box with compass', '2026-09-29', 'Class XII-A', 'S00002', 'Open');
insert into lost_items values ('L00003', 'ID Card', 'Card', 'Class XI-B ID card', '2026-09-30', 'Library', 'S00003', 'Open');
insert into lost_items values ('L00004', 'Water Bottle', 'Bottle', 'Green plastic bottle', '2026-10-01', 'Ground', 'S00004', 'Open');

insert into found_items values ('F00001', 'Water Bottle', 'Bottle', 'Blue steel bottle found near stairs', '2026-09-29', 'Canteen', 'S00003', 'Unclaimed');
insert into found_items values ('F00002', 'Calculator', 'Electronics', 'Casio scientific calculator', '2026-09-30', 'Library', 'S00001', 'Unclaimed');
insert into found_items values ('F00003', 'ID Card', 'Card', 'ID card with blue lanyard', '2026-10-01', 'Library', 'S00002', 'Unclaimed');
