-- Consulta NO optimizada para el reporte de ventas
-- Este es un ejemplo. Reemplázalo con tu consulta real.
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
GROUP BY
    c.name
ORDER BY
    total_sales DESC;