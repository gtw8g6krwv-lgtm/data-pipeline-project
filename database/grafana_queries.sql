-- 1. События по времени (для графика)
SELECT 
    date_trunc('minute', event_time) as time,
    COUNT(*) as events
FROM events 
WHERE event_time > NOW() - INTERVAL '1 hour'
GROUP BY time
ORDER BY time;

-- 2. Распределение по типам событий
SELECT 
    event_type,
    COUNT(*) as count
FROM events 
WHERE event_time > NOW() - INTERVAL '1 hour'
GROUP BY event_type
ORDER BY count DESC;

-- 3. Топ-5 категорий товаров
SELECT 
    product_category,
    COUNT(*) as views
FROM events 
WHERE event_type = 'view' 
    AND event_time > NOW() - INTERVAL '1 hour'
GROUP BY product_category
ORDER BY views DESC
LIMIT 5;

-- 4. Конверсия по воронке
WITH funnel AS (
    SELECT 
        COUNT(DISTINCT session_id) as total_sessions,
        COUNT(DISTINCT CASE WHEN event_type = 'view' THEN session_id END) as views,
        COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN session_id END) as carts,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END) as purchases
    FROM events 
    WHERE event_time > NOW() - INTERVAL '1 hour'
)
SELECT 
    total_sessions,
    views,
    carts,
    purchases,
    ROUND(views::decimal / NULLIF(total_sessions, 0) * 100, 1) as view_rate,
    ROUND(carts::decimal / NULLIF(views, 0) * 100, 1) as cart_rate,
    ROUND(purchases::decimal / NULLIF(carts, 0) * 100, 1) as purchase_rate
FROM funnel;

-- 5. Выручка по часам
SELECT 
    hour,
    total_revenue
FROM hourly_stats 
WHERE hour > NOW() - INTERVAL '24 hours'
ORDER BY hour;
