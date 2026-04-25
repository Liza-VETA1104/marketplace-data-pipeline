-- Создать таблицу sales
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    purchase_date DATE NOT NULL,
    purchase_time_seconds INTEGER NOT NULL,  -- ← добавили
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_item DECIMAL(10, 2),
    discount_per_item DECIMAL(10, 2),
    total_price DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (client_id, product_id, purchase_date, purchase_time_seconds)  -- ← обновили
);

-- Индексы для ускорения запросов 
CREATE INDEX IF NOT EXISTS idx_sales_purchase_date ON sales(purchase_date);
CREATE INDEX IF NOT EXISTS idx_sales_client_id ON sales(client_id);
CREATE INDEX IF NOT EXISTS idx_sales_product_id ON sales(product_id);

COMMENT ON TABLE sales IS 'Таблица продаж маркетплейса';
COMMENT ON COLUMN sales.client_id IS 'Идентификатор клиента';
COMMENT ON COLUMN sales.gender IS 'Пол клиента (M/F)';
COMMENT ON COLUMN sales.purchase_date IS 'Дата покупки';
COMMENT ON COLUMN sales.purchase_time_seconds IS 'Время покупки в секундах от полуночи';
COMMENT ON COLUMN sales.product_id IS 'Идентификатор товара';
COMMENT ON COLUMN sales.quantity IS 'Количество купленных единиц';
COMMENT ON COLUMN sales.price_per_item IS 'Цена за единицу до скидки';
COMMENT ON COLUMN sales.discount_per_item IS 'Скидка на единицу товара';
COMMENT ON COLUMN sales.total_price IS 'Итоговая стоимость покупки';
COMMENT ON COLUMN sales.created_at IS 'Дата и время добавления записи в БД';
