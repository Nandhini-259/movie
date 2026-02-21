SELECT m.title, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY m.title
ORDER BY avg_rating DESC
LIMIT 1;

SELECT g.genre, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN genres g ON r.movie_id = g.movie_id
GROUP BY g.genre
ORDER BY avg_rating DESC
LIMIT 5;

SELECT director, COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;

SELECT m.release_year, AVG(r.rating) AS avg_rating
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY m.release_year
ORDER BY m.release_year;