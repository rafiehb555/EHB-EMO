#!/usr/bin/env python3
"""
EHB Database Test Fixed - Fixed database testing
"""

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def test_database():
    """Test database operations with proper SQL execution"""
    print("🗄️ Testing Database Operations (Fixed)...")
    
    try:
        # Create test database
        engine = create_engine("sqlite:///test.db")
        
        # Test connection with proper SQL execution
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            print(f"✅ Database connection: Working (Result: {row[0]})")
        
        # Test table creation
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    value INTEGER
                )
            """))
            conn.commit()
            print("✅ Table creation: Working")
        
        # Test data insertion
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO test_table (name, value) VALUES (?, ?)"), 
                       ("Test Item", 42))
            conn.commit()
            print("✅ Data insertion: Working")
        
        # Test data retrieval
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM test_table"))
            rows = result.fetchall()
            print(f"✅ Data retrieval: Working (Found {len(rows)} rows)")
        
        # Clean up
        engine.dispose()
        if Path("test.db").exists():
            Path("test.db").unlink()
            print("✅ Database cleanup: Completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    test_database() 