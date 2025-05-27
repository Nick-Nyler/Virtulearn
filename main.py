from lib.database import init_db
from lib.sql_operations import create_tables_sql
from lib.cli import cli

if __name__ == "__main__":
    init_db() 
    cli() 