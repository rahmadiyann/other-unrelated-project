

-- ====================================================================================
-- 2 sql schema
-- ddl --

-- create table on movie db
-- create database
create database movie;
-- create tables
create table actor (
	act_id int primary key,
	act_fname varchar,
	act_lname varchar,
	act_gender varchar
);

create table genres (
	gen_id int primary key,
	gen_title varchar
);

create table director (
	dir_id int primary key,
	dir_fname varchar,
	dir_lname varchar
);

create table movie (
	mov_id int primary key,
	mov_title varchar,
	mov_year int,
	mov_time int,
	mov_lang varchar,
	mov_dt_rel date,
	mov_rel_country varchar
);

create table movie_genres (
	mov_id int,
	gen_id int
);

create table movie_direction (
	dir_id int,
	mov_id int
);

create table reviewer (
	rev_id int primary key,
	rev_name varchar
);

create table rating (
	mov_id int,
	rev_id int,
	rev_stars numeric,
	num_o_ratings int
);

create table movie_cast (
	act_id int,
	mov_id int,
	role varchar
);

-- create database ninja
create database ninja;

-- create table ninja on ninja db
create table ninja (
    id serial primary key,
    nama varchar,
    umur int,
    desa varchar,
    regis_date date
    nilai int
);



-- alter default regis_date to now()
alter table ninja alter column regis_date set default now();


-- HANDSON 1
-- stored procedure for insert data
create or replace procedure insert_ninja(
    in nama varchar,
    in umur int,
    in desa varchar
)
language plpgsql
as $$
begin
    insert into ninja(nama, umur, desa) values(nama, umur, desa);
end;$$;

-- example:
call insert_ninja('naruto', 12, 'konoha', 50);
call insert_ninja('sasuke', 12, 'konoha', 90);
call insert_ninja('sakura', 12, 'konoha', 80);
call insert_ninja('kakashi', 30, 'konoha', 70);
call insert_ninja('itachi', 30, 'konoha', 85);
call insert_ninja('madara', 30, 'konoha', 92);

-- HANDSON 2
-- stored procedure for deduce nilai with given id and amount to deduce
create or replace procedure deduce_nilai(
    in id int,
    in amount int
)
language plpgsql
as $$
begin
    update ninja set nilai = nilai - amount where id = id;
end;$$;

-- example:
call deduce_nilai(1, 10);
call deduce_nilai(2, 10);

-- HANDSON 3
-- ROW_NUMBER() based on name alphabetically
select *, row_number() over(order by nama) as row_number from ninja;

-- HANDSON 4
-- most favorite director for each genre (assuming the highest average rating)
SELECT 
    g.gen_title AS genre,
    d.dir_fname AS director_first_name,
    d.dir_lname AS director_last_name,
    AVG(r.rev_stars) AS avg_rating
FROM 
    genres g
JOIN 
    movie_genres mg ON g.gen_id = mg.gen_id
JOIN 
    movie m ON mg.mov_id = m.mov_id
JOIN 
    movie_direction md ON m.mov_id = md.mov_id
JOIN 
    director d ON md.dir_id = d.dir_id
JOIN 
    rating r ON m.mov_id = r.mov_id
GROUP BY 
    g.gen_id, g.gen_title, d.dir_id, d.dir_fname, d.dir_lname
HAVING 
    AVG(r.rev_stars) = (
        SELECT 
            MAX(avg_rating)
        FROM (
            SELECT 
                AVG(r.rev_stars) AS avg_rating
            FROM 
                movie_genres mg2
            JOIN 
                movie m2 ON mg2.mov_id = m2.mov_id
            JOIN 
                movie_direction md2 ON m2.mov_id = md2.mov_id
            JOIN 
                director d2 ON md2.dir_id = d2.dir_id
            JOIN 
                rating r2 ON m2.mov_id = r2.mov_id
            WHERE 
                mg2.gen_id = g.gen_id
            GROUP BY 
                d2.dir_id
        ) AS avg_ratings_per_director
    );

-- HANDSON 5
-- find movie title that has a character named Alice Harford
SELECT 
    m.mov_title
FROM 
    movie m
JOIN 
    movie_cast mc ON m.mov_id = mc.mov_id
WHERE 
    mc.role = 'Alice Harford';

-- HANDSON 6
-- find actor that has played as Sean Maguire, create an index the for query, show explain result before and after

-- before index
EXPLAIN
SELECT 
    a.act_fname,
    a.act_lname
FROM 
    actor a
JOIN 
    movie_cast mc ON a.act_id = mc.act_id
WHERE 
    mc.role = 'Sean Maguire';

                                   QUERY PLAN                                    
---------------------------------------------------------------------------------
 Nested Loop  (cost=0.15..9.48 rows=1 width=64)
   ->  Seq Scan on movie_cast mc  (cost=0.00..1.29 rows=1 width=4)
         Filter: ((role)::text = 'Sean Maguire'::text)
   ->  Index Scan using actor_pkey on actor a  (cost=0.15..8.17 rows=1 width=68)
         Index Cond: (act_id = mc.act_id)
(5 rows)


-- create index
CREATE INDEX idx_role ON movie_cast(role);

-- after index
EXPLAIN
SELECT 
    a.act_fname,
    a.act_lname
FROM 
    actor a
JOIN 
    movie_cast mc ON a.act_id = mc.act_id
WHERE 
    mc.role = 'Sean Maguire';

                                       QUERY PLAN                                    
---------------------------------------------------------------------------------
 Nested Loop  (cost=0.15..9.48 rows=1 width=64)
   ->  Seq Scan on movie_cast mc  (cost=0.00..1.29 rows=1 width=4)
         Filter: ((role)::text = 'Sean Maguire'::text)
   ->  Index Scan using actor_pkey on actor a  (cost=0.15..8.17 rows=1 width=68)
         Index Cond: (act_id = mc.act_id)
(5 rows)
