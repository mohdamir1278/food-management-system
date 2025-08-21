select city, 'providers' as entity_type, count(*) as total
from providers
group by city
union all 
select city, 'receivers' as entity_type, count(*) as total
from receivers
group by city
order by city, entity_type

select p.type as provider_type,
sum(f.quantity) as total_quantity
from food_inventory f
inner join providers p
on f.provider_id=p.provider_id
group by p.type
order by total_quantity desc

select * from providers

select name,address,city,contact from providers
where city='city'

select r.name as receive_name, count(c.claim_id) as total_claim
from claims c
inner join receivers r
on r.receiver_id=c.receiver_id
group by r.name
order by total_claim desc


SELECT
    p.name AS provider_name,
    SUM(f.quantity) AS total_quantity
FROM food_inventory f
JOIN providers p
    ON f.provider_id = p.provider_id
GROUP BY p.name
ORDER BY total_quantity DESC;

select location as city,
count(*) as total_listings
from food_inventory
group by location
order by total_listings desc;

SELECT
    food_type,
    COUNT(*) AS total_listings
FROM food_inventory
GROUP BY food_type
ORDER BY total_listings DESC;


SELECT
    f.food_id,
    f.food_name,
    COUNT(c.claim_id) AS total_claims
FROM claims c
JOIN food_inventory f
    ON c.food_id = f.food_id
GROUP BY f.food_id, f.food_name
ORDER BY total_claims DESC;

SELECT
    p.provider_id,
    p.name AS provider_name,
    COUNT(c.claim_id) AS successful_claims
FROM claims c
JOIN food_inventory f
    ON c.food_id = f.food_id
JOIN providers p
    ON f.provider_id = p.provider_id
WHERE c.status = 'completed'
GROUP BY p.provider_id, p.name
ORDER BY successful_claims DESC
LIMIT 1;

select c.status  ,count(c.claim_id)as claim from claims c
join food_inventory f
on c.food_id=f.food_id
-- join providers p
-- on f.provider_id = p.provider_id
where c.status='completed'
group by c.status 
order by claim desc



select * from claims





SELECT
    status,
    COUNT(*) AS claim_count,
    ROUND( (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER()), 2 ) AS percentage
FROM claims
GROUP BY status
ORDER BY percentage DESC;


SELECT
    r.receiver_id,
    r.name AS receiver_name,
    ROUND(AVG(f.quantity), 2) AS avg_quantity_claimed
FROM claims c
JOIN food_inventory f
    ON c.food_id = f.food_id
JOIN receivers r
    ON c.receiver_id = r.receiver_id
GROUP BY r.receiver_id, r.name
ORDER BY avg_quantity_claimed DESC;

SELECT
    f.meal_type,
    COUNT(c.claim_id) AS total_claims
FROM claims c
JOIN food_inventory f
    ON c.food_id = f.food_id
GROUP BY f.meal_type
ORDER BY total_claims DESC;

SELECT
    p.provider_id,
    p.name AS provider_name,
    SUM(f.quantity) AS total_quantity_donated
FROM food_inventory f
JOIN providers p
    ON f.provider_id = p.provider_id
GROUP BY p.provider_id, p.name
ORDER BY total_quantity_donated DESC;



