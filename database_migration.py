#!/usr/bin/env python3
"""
EHB-5 Database Migration System
Production database migration and setup
"""

import sqlite3
import psycopg2
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from database import db


class DatabaseMigration:
    """Database migration system for production deployment"""

    def __init__(self):
        self.migration_config = {
            "source": {
                "type": "sqlite",
                "path": "ehb5.db"
            },
            "target": {
                "type": "postgresql",
                "host": os.getenv("DB_HOST", "localhost"),
                "port": os.getenv("DB_PORT", "5432"),
                "database": os.getenv("DB_NAME", "ehb5_production"),
                "user": os.getenv("DB_USER", "ehb5_user"),
                "password": os.getenv("DB_PASSWORD", "")
            },
            "migration_options": {
                "backup_before_migration": True,
                "validate_data": True,
                "create_indexes": True,
                "optimize_queries": True
            }
        }
        self.migration_log = []

    def backup_sqlite_database(self) -> Dict[str, Any]:
        """Create backup of SQLite database"""
        print("💾 Creating SQLite database backup...")

        try:
backup_path = f"ehb5_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

            # Connect to source database
            source_conn = sqlite3.connect(
                self.migration_config["source"]["path"])
            source_cursor = source_conn.cursor()

            # Create backup
            backup_conn = sqlite3.connect(backup_path)
            source_conn.backup(backup_conn)

            # Verify backup
            backup_cursor = backup_conn.cursor()
            backup_cursor.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = backup_cursor.fetchone()[0]

            source_cursor.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            source_table_count = source_cursor.fetchone()[0]

            if table_count == source_table_count:
                print(f"✅ Backup created successfully: {backup_path}")
                print(f"📊 Tables backed up: {table_count}")

                self.migration_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "action": "backup_created",
                    "backup_path": backup_path,
                    "table_count": table_count
                })

                return {
                    "status": "success",
                    "backup_path": backup_path,
                    "table_count": table_count
                }
            else:
                print("❌ Backup verification failed")
                return {
                    "status": "error",
                    "message": "Backup verification failed"}

        except Exception as e:
            print(f"❌ Backup error: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if 'source_conn' in locals():
                source_conn.close()
            if 'backup_conn' in locals():
                backup_conn.close()

    def analyze_sqlite_schema(self) -> Dict[str, Any]:
        """Analyze SQLite database schema"""
        print("🔍 Analyzing SQLite database schema...")

        try:
            conn = sqlite3.connect(self.migration_config["source"]["path"])
            cursor = conn.cursor()

            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            schema_analysis = {
                "tables": {},
                "total_tables": len(tables),
                "total_records": 0
            }

            for table in tables:
                # Get table info
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()

                # Get record count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                record_count = cursor.fetchone()[0]

                schema_analysis["tables"][table] = {
                    "columns": [col[1] for col in columns],
                    "column_types": [col[2] for col in columns],
                    "record_count": record_count
                }
                schema_analysis["total_records"] += record_count

            print(f"✅ Schema analysis complete")
            print(f"📊 Tables found: {schema_analysis['total_tables']}")
            print(f"📊 Total records: {schema_analysis['total_records']}")

            return {"status": "success", "schema": schema_analysis}

        except Exception as e:
            print(f"❌ Schema analysis error: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if 'conn' in locals():
                conn.close()

    def create_postgresql_schema(
            self, schema_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create PostgreSQL schema based on SQLite analysis"""
        print("🏗️ Creating PostgreSQL schema...")

        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host=self.migration_config["target"]["host"],
                port=self.migration_config["target"]["port"],
                database=self.migration_config["target"]["database"],
                user=self.migration_config["target"]["user"],
                password=self.migration_config["target"]["password"]
            )
            cursor = conn.cursor()

            # Create tables
            created_tables = []
for table_name, table_info in schema_analysis["schema"]["tables"].items(
            ):
                columns = table_info["columns"]
                column_types = table_info["column_types"]

                # Map SQLite types to PostgreSQL types
                pg_column_definitions = []
                for i, (col_name, col_type) in enumerate(
                        zip(columns, column_types)):
                    pg_type = self._map_sqlite_to_postgresql_type(col_type)
                    pg_column_definitions.append(f"{col_name} {pg_type}")

                # Create table
                create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(pg_column_definitions)}
                );
                """

                cursor.execute(create_table_sql)
                created_tables.append(table_name)

            # Create indexes for better performance
            if self.migration_config["migration_options"]["create_indexes"]:
                self._create_postgresql_indexes(
                    cursor, schema_analysis["schema"]["tables"])

            conn.commit()

            print(f"✅ PostgreSQL schema created successfully")
            print(f"📊 Tables created: {len(created_tables)}")

            return {
                "status": "success",
                "created_tables": created_tables,
                "total_tables": len(created_tables)
            }

        except Exception as e:
            print(f"❌ PostgreSQL schema creation error: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if 'conn' in locals():
                conn.close()

    def _map_sqlite_to_postgresql_type(self, sqlite_type: str) -> str:
        """Map SQLite data types to PostgreSQL types"""
        type_mapping = {
            "INTEGER": "INTEGER",
            "REAL": "DOUBLE PRECISION",
            "TEXT": "TEXT",
            "BLOB": "BYTEA",
            "VARCHAR": "VARCHAR",
            "DATETIME": "TIMESTAMP",
            "BOOLEAN": "BOOLEAN"
        }

        # Handle common variations
        sqlite_type_upper = sqlite_type.upper()

        if "INT" in sqlite_type_upper:
            return "INTEGER"
        elif "REAL" in sqlite_type_upper or "FLOAT" in sqlite_type_upper:
            return "DOUBLE PRECISION"
        elif "TEXT" in sqlite_type_upper or "VARCHAR" in sqlite_type_upper:
            return "TEXT"
        elif "BLOB" in sqlite_type_upper:
            return "BYTEA"
elif "DATETIME" in sqlite_type_upper or "TIMESTAMP" in sqlite_type_upper:
            return "TIMESTAMP"
        elif "BOOLEAN" in sqlite_type_upper:
            return "BOOLEAN"
        else:
            return "TEXT"  # Default to TEXT for unknown types

    def _create_postgresql_indexes(self, cursor, tables: Dict[str, Any]):
        """Create indexes for better PostgreSQL performance"""
        print("🔍 Creating PostgreSQL indexes...")

        # Common index patterns
        index_patterns = {
            "users": ["username", "email"],
            "projects": ["user_id", "created_at"],
            "files": ["project_id", "file_type"],
            "system_logs": ["timestamp", "level"],
            "security_events": ["timestamp", "event_type"]
        }

        for table_name, table_info in tables.items():
            if table_name in index_patterns:
                for column in index_patterns[table_name]:
                    if column in table_info["columns"]:
                        index_name = f"idx_{table_name}_{column}"
                        try:
                            cursor.execute(
f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column})")
                        except Exception as e:
                            print(
                                f"⚠️ Could not create index {index_name}: {e}")

        print("✅ PostgreSQL indexes created")

    def migrate_data(self, schema_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate data from SQLite to PostgreSQL"""
        print("🔄 Migrating data from SQLite to PostgreSQL...")

        try:
            # Connect to both databases
            sqlite_conn = sqlite3.connect(
                self.migration_config["source"]["path"])
            sqlite_cursor = sqlite_conn.cursor()

            pg_conn = psycopg2.connect(
                host=self.migration_config["target"]["host"],
                port=self.migration_config["target"]["port"],
                database=self.migration_config["target"]["database"],
                user=self.migration_config["target"]["user"],
                password=self.migration_config["target"]["password"]
            )
            pg_cursor = pg_conn.cursor()

            migration_stats = {
                "tables_migrated": 0,
                "total_records_migrated": 0,
                "errors": []
            }

for table_name, table_info in schema_analysis["schema"]["tables"].items(
            ):
                try:
                    print(f"📦 Migrating table: {table_name}")

                    # Get all data from SQLite
                    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
                    rows = sqlite_cursor.fetchall()

                    if rows:
                        # Prepare insert statement
                        columns = table_info["columns"]
                        placeholders = ", ".join(["%s"] * len(columns))
insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES
    ({placeholders})"

                        # Insert data into PostgreSQL
                        pg_cursor.executemany(insert_sql, rows)

                        migration_stats["tables_migrated"] += 1
                        migration_stats["total_records_migrated"] += len(rows)

                        print(
f"✅ Migrated {len(rows)} records from {table_name}")
                    else:
                        print(f"ℹ️ Table {table_name} is empty")

                except Exception as e:
                    error_msg = f"Error migrating table {table_name}: {e}"
                    print(f"❌ {error_msg}")
                    migration_stats["errors"].append(error_msg)

            # Commit changes
            pg_conn.commit()

            print(f"✅ Data migration completed")
            print(f"📊 Tables migrated: {migration_stats['tables_migrated']}")
            print(
f"📊 Total records migrated: {migration_stats['total_records_migrated']}")

            if migration_stats["errors"]:
                print(
                    f"⚠️ Errors encountered: {len(migration_stats['errors'])}")

            return {
                "status": "success",
                "stats": migration_stats
            }

        except Exception as e:
            print(f"❌ Data migration error: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if 'sqlite_conn' in locals():
                sqlite_conn.close()
            if 'pg_conn' in locals():
                pg_conn.close()

    def validate_migration(
            self, schema_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the migration by comparing record counts"""
        print("🔍 Validating migration...")

        try:
            # Connect to both databases
            sqlite_conn = sqlite3.connect(
                self.migration_config["source"]["path"])
            sqlite_cursor = sqlite_conn.cursor()

            pg_conn = psycopg2.connect(
                host=self.migration_config["target"]["host"],
                port=self.migration_config["target"]["port"],
                database=self.migration_config["target"]["database"],
                user=self.migration_config["target"]["user"],
                password=self.migration_config["target"]["password"]
            )
            pg_cursor = pg_conn.cursor()

            validation_results = {
                "tables_validated": 0,
                "matching_records": 0,
                "mismatches": [],
                "overall_success": True
            }

for table_name, table_info in schema_analysis["schema"]["tables"].items(
            ):
                try:
                    # Count records in SQLite
                    sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    sqlite_count = sqlite_cursor.fetchone()[0]

                    # Count records in PostgreSQL
                    pg_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    pg_count = pg_cursor.fetchone()[0]

                    if sqlite_count == pg_count:
                        validation_results["matching_records"] += 1
                        print(f"✅ {table_name}: {sqlite_count} records match")
                    else:
                        validation_results["mismatches"].append({
                            "table": table_name,
                            "sqlite_count": sqlite_count,
                            "postgresql_count": pg_count
                        })
                        validation_results["overall_success"] = False
                        print(
f"❌ {table_name}: {sqlite_count} vs {pg_count} records")

                    validation_results["tables_validated"] += 1

                except Exception as e:
                    print(f"❌ Validation error for {table_name}: {e}")
                    validation_results["overall_success"] = False

            if validation_results["overall_success"]:
                print("✅ Migration validation successful!")
            else:
                print("⚠️ Migration validation found mismatches")

            return {
                "status": "success",
                "validation": validation_results
            }

        except Exception as e:
            print(f"❌ Validation error: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if 'sqlite_conn' in locals():
                sqlite_conn.close()
            if 'pg_conn' in locals():
                pg_conn.close()

    def generate_migration_report(self, migration_data: Dict[str, Any]) -> str:
        """Generate comprehensive migration report"""
        report = f"""
# EHB-5 Database Migration Report

## Migration Summary
- **Timestamp**: {datetime.now().isoformat()}
- **Source**: SQLite ({self.migration_config['source']['path']})
- **Target**: PostgreSQL ({self.migration_config['target']['database']})
- **Status**: {migration_data.get('status', 'Unknown')}

## Migration Statistics
- **Tables Migrated**: {migration_data.get('stats', {}).get('tables_migrated',
    0)}
- **Total Records**: {migration_data.get('stats',
    {}).get('total_records_migrated', 0)}
- **Errors**: {len(migration_data.get('stats', {}).get('errors', []))}

## Validation Results
- **Tables Validated**: {migration_data.get('validation',
    {}).get('tables_validated', 0)}
- **Matching Records**: {migration_data.get('validation',
    {}).get('matching_records', 0)}
- **Overall Success**: {'✅ Yes' if migration_data.get('validation',
    {}).get('overall_success', False) else '❌ No'}

## Next Steps
1. Update application configuration to use PostgreSQL
2. Test application with new database
3. Set up automated backups
4. Monitor performance
5. Remove SQLite database (after verification)

## Configuration
```bash
# PostgreSQL Connection String
DATABASE_URL=postgresql://{self.migration_config['target']['user']}:{self.migration_config['target']['password']}@{self.migration_config['target']['host']}:{self.migration_config['target']['port']}/{self.migration_config['target']['database']}
```

Migration completed at: {datetime.now().isoformat()}
"""

        # Save report
        with open("database_migration_report.md", "w") as f:
            f.write(report)

        print("✅ Migration report generated: database_migration_report.md")
        return report

    def run_full_migration(self) -> Dict[str, Any]:
        """Run the complete database migration process"""
        print("🚀 Starting EHB-5 Database Migration")
        print("=" * 50)

        # Step 1: Backup SQLite database
        backup_result = self.backup_sqlite_database()
        if backup_result["status"] != "success":
            return {"status": "error", "message": "Backup failed"}

        # Step 2: Analyze SQLite schema
        schema_result = self.analyze_sqlite_schema()
        if schema_result["status"] != "success":
            return {"status": "error", "message": "Schema analysis failed"}

        # Step 3: Create PostgreSQL schema
        schema_creation_result = self.create_postgresql_schema(
            schema_result["schema"])
        if schema_creation_result["status"] != "success":
            return {
                "status": "error",
                "message": "PostgreSQL schema creation failed"}

        # Step 4: Migrate data
        migration_result = self.migrate_data(schema_result["schema"])
        if migration_result["status"] != "success":
            return {"status": "error", "message": "Data migration failed"}

        # Step 5: Validate migration
        validation_result = self.validate_migration(schema_result["schema"])
        if validation_result["status"] != "success":
            return {
                "status": "error",
                "message": "Migration validation failed"}

        # Step 6: Generate report
        report = self.generate_migration_report({
            "status": "success",
            "stats": migration_result.get("stats", {}),
            "validation": validation_result.get("validation", {})
        })

        # Final result
        final_result = {
            "status": "success",
            "backup": backup_result,
            "schema_analysis": schema_result,
            "schema_creation": schema_creation_result,
            "migration": migration_result,
            "validation": validation_result,
            "report": "database_migration_report.md"
        }

        print("\n" + "=" * 50)
        print("🎉 DATABASE MIGRATION COMPLETED SUCCESSFULLY!")
        print(
f"📊 Records migrated: {migration_result.get('stats',
    {}).get('total_records_migrated', 0)}")
        print(
f"✅ Validation: {'Passed' if validation_result.get('validation',
    {}).get('overall_success', False) else 'Failed'}")
        print("📋 Report: database_migration_report.md")
        print("=" * 50)

        return final_result


# Global database migration instance
database_migration = DatabaseMigration()
