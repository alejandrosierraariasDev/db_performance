-- Consulta OPTIMIZADA para el inventario de películas
-- Este es un ejemplo. Reemplázalo con tu consulta optimizada real.
SELECT
    f.title,
    COUNT(i.inventory_id) AS total_copies
FROM
    film f
JOIN
    inventory i ON f.film_id = i.film_id
GROUP BY
    f.title
ORDER BY
    total_copies DESC;