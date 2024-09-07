-- nama lengkap: rahmadiyan muhammad

-- case 1 (find each genre of each movie)
SELECT 
    m.mov_title AS movie_title,
    g.gen_title AS genre_title
FROM 
    movie m
JOIN 
    movie_genres mg ON m.mov_id = mg.mov_id
JOIN 
    genres g ON mg.gen_id = g.gen_id
ORDER BY 
    m.mov_title, g.gen_title;

-- case 2 (Count the number of male and female actor)
SELECT 
    act_gender AS gender,
    COUNT(*) AS count
FROM 
    actor
GROUP BY 
    act_gender;

-- case 3 (Find actor that has played in more than one movie)
SELECT 
    a.act_fname,
    a.act_lname,
    COUNT(mc.mov_id) AS movie_count
FROM 
    actor a
JOIN 
    movie_cast mc ON a.act_id = mc.act_id
GROUP BY 
    a.act_id, a.act_fname, a.act_lname
HAVING 
    COUNT(mc.mov_id) > 1;

-- case 4 (Find a movie with the lowest rating)
SELECT 
    m.mov_title,
    r.rev_stars
FROM 
    movie m
JOIN 
    rating r ON m.mov_id = r.mov_id
ORDER BY 
    r.rev_stars ASC
LIMIT 1;

-- case 5 (Find what year that has most movies (movies of each year))
SELECT 
    mov_year,
    COUNT(*) AS movie_count
FROM
    movie
GROUP BY
    mov_year
ORDER BY
    movie_count DESC
LIMIT 1;
