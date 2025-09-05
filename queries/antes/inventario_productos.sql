-- Consulta NO optimizada para el inventario de películas
-- Este es un ejemplo. Reemplázalo con tu consulta real.
SELECT
    f.title,
    (SELECT COUNT(*) FROM inventory WHERE film_id = f.film_id) AS total_copies
FROM
    film f
ORDER BY
    total_copies DESC;