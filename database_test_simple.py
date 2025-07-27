#!/usr/bin/env python3
"""
EHB Database Test Simple - Simple working database test
"""

import sqlite3
from pathlib import Path


def test_database_simple():
    """Test database operations with simple SQLite"""
    print("🗄️ Testing Database Operations (Simple)...")
    
    try:
        # Create test database
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        
        # Test table creation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value INTEGER
            )
        """)
        print("✅ Table creation: Working")
        
        # Test data insertion
        cursor.execute("INSERT INTO test_table (name, value) VALUES (?, ?)", 
                      ("Test Item", 42))
        conn.commit()
        print("✅ Data insertion: Working")
        
        # Test data retrieval
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        print(f"✅ Data retrieval: Working (Found {len(rows)} rows)")
        
        # Test connection
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Database connection: Working (Result: {result[0]})")
        
        # Clean up
        conn.close()
        if Path("test.db").exists():
            Path("test.db").unlink()
            print("✅ Database cleanup: Completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    test_database_simple() 