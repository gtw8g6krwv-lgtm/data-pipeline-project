CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_time TIMESTAMP NOT NULL DEFAULT NOW(),
    event_type VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    session_id VARCHAR(100),
    product_id INT,
    product_category VARCHAR(100),
    price DECIMAL(10,2),
    user_agent TEXT,
    ip_address VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS hourly_stats (
    hour TIMESTAMP PRIMARY KEY,
    total_events INT DEFAULT 0,
    view_events INT DEFAULT 0,
    cart_events INT DEFAULT 0,
    purchase_events INT DEFAULT 0,
    total_revenue DECIMAL(10,2) DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_events_time ON events(event_time);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id);

-- Комментарии к таблицам
COMMENT ON TABLE events IS 'Сырые события интернет-магазина';
COMMENT ON TABLE hourly_stats IS 'Агрегированная статистика по часам';
