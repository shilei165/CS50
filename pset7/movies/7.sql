SELECT movies.title,ratings.rating FROM movies INNER JOIN ratings WHERE (movies.id = ratings.movie_id and movies.year = 2010) ORDER BY ratings.rating DESC, movies.title ASC;