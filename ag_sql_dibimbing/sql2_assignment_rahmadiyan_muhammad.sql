-- nama lengkap: Rahmadiyan Muhammad

-- case 3 ( create table  students )

CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR DEFAULT NULL,
    email VARCHAR UNIQUE NOT NULL,
    age INTEGER DEFAULT 18,
    gender VARCHAR CHECK (gender IN ('male', 'female')),
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- case 4 ( create procedure to return sum movie with given genre parameter )
CREATE OR REPLACE FUNCTION sum_movie_by_genre(
    genre VARCHAR
)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(m.mov_id)
        FROM movie m
        JOIN movie_genres mg ON m.mov_id = mg.mov_id
        JOIN genres g ON mg.gen_id = g.gen_id
        WHERE g.gen_title = genre
);
END;
$$ LANGUAGE plpgsql;

-- case 5 (tulis query yang mengembalikan nama dan desa, gunakan email sebagai filter. Buat indeks yang tepat untuk memenuhi query, berikan hasil penjelasan sebelum dan sesudah pembuatan indeks.)
verceldb=> EXPLAIN SELECT nama, desa FROM ninja WHERE email='sasuke@mail.com';

                      QUERY PLAN                       
-------------------------------------------------------
 Seq Scan on ninja  (cost=0.00..17.50 rows=3 width=64)
   Filter: ((email)::text = 'sasuke@mail.com'::text)
(2 rows)

verceldb=> create index nama_desa_idx on ninja(nama, desa);
CREATE INDEX

verceldb=> set enable_seqscan=off;
SET

verceldb=> EXPLAIN SELECT nama, desa FROM ninja WHERE email='sasuke@mail.com';
                                QUERY PLAN                                
--------------------------------------------------------------------------
 Seq Scan on ninja  (cost=10000000000.00..10000000001.04 rows=1 width=64)
   Filter: ((email)::text = 'sasuke@mail.com'::text)
(2 rows)

-- case 6 (Temukan yang paling favorit (rating tertinggi) untuk setiap genre (menggunakan fungsi rank() window).

SELECT
    mov_id,
    gen_title,
    avg_rating,
    movie_rank
FROM (
    SELECT
        m.mov_id,
        g.gen_title,
        AVG(r.rev_stars) AS avg_rating,
        RANK() OVER (PARTITION BY gen_title ORDER BY AVG(r.rev_stars) DESC) AS movie_rank
    FROM
        movie m
    JOIN
        movie_genres mg ON m.mov_id = mg.mov_id
    JOIN
        genres g ON mg.gen_id = g.gen_id
    JOIN
        rating r ON m.mov_id = r.mov_id
    GROUP BY
        m.mov_id,
        g.gen_title
) AS ranked_movies
WHERE
    movie_rank = 1;

-- case 7 (Temukan judul film yang disutradarai oleh James Cameron (rekomendasi output: director name, movie title))

SELECT
    CONCAT(d.dir_fname, ' ', d.dir_lname) AS director_name,
    m.mov_title
FROM
    movie m
JOIN
    movie_direction md ON m.mov_id = md.mov_id
JOIN
    director d ON md.dir_id = d.dir_id
WHERE
    d.dir_fname = 'James'
    AND d.dir_lname = 'Cameron';

-- case 8 (List semua nama depan dari aktor dan sutradara (hanya satu kolom, tanpa pengulangan, dan diurutkan sesuai alfabet))
SELECT DISTINCT
    act_fname
FROM
    actor
UNION
SELECT DISTINCT
    dir_fname
FROM
    director
ORDER BY 
    act_fname;

-- case 9 (Temukan berapa jumlah film yang bergenre Mystery, Drama, dan Adventure (rekomendasi output: genre title, number of movies)
SELECT
    g.gen_title AS genre_title,
    COUNT(m.mov_id) AS number_of_movies
FROM
    movie m
JOIN
    movie_genres mg ON m.mov_id = mg.mov_id
JOIN
    genres g ON mg.gen_id = g.gen_id
WHERE
    g.gen_title IN ('Mystery', 'Drama', 'Adventure')
GROUP BY
    g.gen_title;

-- case 10 (Berikan label terhadap durasi film dengan menggunakan aturan di bawah ini:
-- mov_time < 100 = short movie
-- mov_time > 130 = long movie
-- mov_time between 100 and 130 = normal movie
-- Kemudian, hitung jumlah film per label tersebut.
-- (rekomendasi output: label duration, number of movies)

SELECT
    CASE
        WHEN m.mov_time < 100 THEN 'short movie'
        WHEN m.mov_time > 130 THEN 'long movie'
        ELSE 'normal movie'
    END AS label_duration,
    COUNT(m.mov_id) AS number_of_movies
FROM
    movie m
GROUP BY
    label_duration;
    