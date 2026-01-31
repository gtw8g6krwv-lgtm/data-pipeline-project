#!/usr/bin/env python3
import time
import random
from datetime import datetime
import logging
import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Запуск генератора")
    time.sleep(20)
    
    try:
        conn = psycopg2.connect(
            host='postgres',
            database='shop',
            user='admin',
            password='admin123',
            port=5432
        )
        conn.autocommit = True
        cursor = conn.cursor()
        logger.info("Подключено к PostgreSQL")
    except Exception as e:
        logger.error(f"Ошибка подключения: {e}")
        return
    
    event_types = ['view', 'add_to_cart', 'purchase']
    product_categories = ['electronics', 'books', 'clothing', 'home']
    
    event_count = 0
    user_ids = list(range(1, 101))
    product_ids = list(range(1, 51))
    
    logger.info("Генерация событий")
    
    try:
        while True:
            for _ in range(random.randint(1, 3)):
                event_time = datetime.now()
                event_type = random.choice(event_types)
                user_id = random.choice(user_ids)
                product_id = random.choice(product_ids)
                price = round(random.uniform(10, 1000), 2) if event_type == 'purchase' else None
                
                try:
                    cursor.execute("""
                        INSERT INTO events 
                        (event_time, event_type, user_id, product_id, price, product_category)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        event_time,
                        event_type,
                        user_id,
                        product_id,
                        price,
                        random.choice(product_categories)
                    ))
                    
                    event_count += 1
                    
                    if event_count % 10 == 0:
                        logger.info(f"Событий: {event_count}")
                        
                except Exception as e:
                    logger.error(f"Ошибка: {e}")
            
            time.sleep(random.uniform(1, 3))
            
    except KeyboardInterrupt:
        logger.info("Остановка")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
