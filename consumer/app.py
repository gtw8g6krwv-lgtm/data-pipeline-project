#!/usr/bin/env python3
import json
import time
import logging
from datetime import datetime
import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventConsumer:
    def __init__(self):
        self.db_connection = psycopg2.connect(
            host='postgres',
            database='shop',
            user='admin',
            password='admin123'
        )
        self.db_connection.autocommit = True
        self.cursor = self.db_connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                event_time TIMESTAMP NOT NULL,
                event_type VARCHAR(50) NOT NULL,
                user_id INT NOT NULL,
                product_id INT,
                price DECIMAL(10,2)
            )
        """)
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_time ON events(event_time)
        """)
    
    def save_event_to_db(self, event):
        try:
            event_time = datetime.fromisoformat(event['event_time'].replace('Z', '+00:00'))
            self.cursor.execute("""
                INSERT INTO events (event_time, event_type, user_id, product_id, price)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                event_time,
                event['event_type'],
                event['user_id'],
                event.get('product_id'),
                event.get('price')
            ))
            return True
        except Exception:
            return False
    
    def run(self):
        logger.info("Consumer запущен")
        
        try:
            while True:
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Остановка consumer...")
        finally:
            self.cursor.close()
            self.db_connection.close()

if __name__ == "__main__":
    time.sleep(30)
    consumer = EventConsumer()
    consumer.run()
