// Count by content type
SELECT type, COUNT(*) 
FROM curated
GROUP BY type;

//Movies added per year
SELECT year(date_added) AS year, COUNT(*) 
FROM curated
WHERE type = 'Movie'
GROUP BY year
ORDER BY year;

// Top countries producing content
SELECT country, COUNT(*) 
FROM curated
GROUP BY country
ORDER BY COUNT(*) DESC
LIMIT 10;
