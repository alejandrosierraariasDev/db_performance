-- Consulta OPTIMIZADA para el reporte de ventas
-- Este es un ejemplo. Reemplázalo con tu consulta optimizada real.
-- Nota: Aquí se añade un filtro de fecha para simular un escenario donde
-- la optimización podría ser más evidente al reducir el volumen de datos.
SELECT
    c.name AS category,
    SUM(p.amount) AS total_sales
FROM
    category c
JOIN
    film_category fc ON c.category_id = fc.category_id
JOIN
    film f ON fc.film_id = f.film_id
JOIN
    inventory i ON f.film_id = i.film_id
JOIN
    rental r ON i.inventory_id = r.inventory_id
JOIN
    payment p ON r.rental_id = p.rental_id
WHERE
    r.rental_date BETWEEN '2005-05-01' AND '2005-06-01' -- Ejemplo de filtro para reducir datos
GROUP BY
    c.name
ORDER BY
    total_sales DESC;