SELECT DISTINCT(name) FROM people WHERE id IN
(SELECT person_id FROM stars Where movie_id IN
(SELECT movie_id FROM stars Where person_id IN
(SELECT id FROM people WHERE name = 'Kevin Bacon' and
(SELECT id FROM people WHERE birth = 1958))))
 INTERSECT
 SELECT DISTINCT(name) FROM people WHERE id and name IS NOT 'Kevin Bacon' IN
(SELECT person_id FROM stars Where movie_id IN
(SELECT movie_id FROM stars Where person_id IN
(SELECT id FROM people WHERE name IS NOT 'Kevin Bacon')))
 ORDER BY NAME;