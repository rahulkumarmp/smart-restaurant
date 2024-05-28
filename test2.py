import pymysql
import psycopg2

# MySQL connection parameters
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = ''  # Assuming an empty password
mysql_db = 'gnt_test'

# PostgreSQL connection parameters
pg_host = 'localhost'
pg_user = 'admin'
pg_password = ''  # Adjust if needed
pg_db = 'gnt_test'

try:
    # Connect to MySQL
    mysql_conn = pymysql.connect(host=mysql_host,
                                 user=mysql_user,
                                 password=mysql_password,
                                 db=mysql_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(host=pg_host,
                               dbname=pg_db,
                               user=pg_user,
                               password=pg_password)
    pg_cursor = pg_conn.cursor()

    # Create state and district tables in PostgreSQL
    pg_cursor.execute("""
        CREATE TABLE IF NOT EXISTS state (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        );
    """)

    pg_cursor.execute("""
        CREATE TABLE IF NOT EXISTS district (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            state_id INTEGER,
            FOREIGN KEY (state_id) REFERENCES state(id)
        );
    """)

    # Alter testuser table to include state_id and district_id
    pg_cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_attribute WHERE attrelid = 'testuser'::regclass AND attname = 'state_id') THEN
                ALTER TABLE testuser ADD COLUMN state_id INTEGER;
                ALTER TABLE testuser ADD CONSTRAINT fk_testuser_state FOREIGN KEY (state_id) REFERENCES state(id);
            END IF;
            IF NOT EXISTS (SELECT FROM pg_attribute WHERE attrelid = 'testuser'::regclass AND attname = 'district_id') THEN
                ALTER TABLE testuser ADD COLUMN district_id INTEGER;
                ALTER TABLE testuser ADD CONSTRAINT fk_testuser_district FOREIGN KEY (district_id) REFERENCES district(id);
            END IF;
        END
        $$;
    """)

    with mysql_conn.cursor() as cursor:
        # Populate state table from tbl_province
        cursor.execute("SELECT DISTINCT id, name FROM tbl_province")
        for row in cursor.fetchall():
            # Insert state data, avoiding duplicates based on the state name
            pg_cursor.execute("""
                INSERT INTO state (id, name)
                VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (row['id'], row['name']))

        # Populate district table from tbl_zone
        cursor.execute("SELECT DISTINCT id, name FROM tbl_zone")
        for row in cursor.fetchall():
            # Attempt to insert district data, avoiding duplicates based on the district name
            # Here, it's not clear how state_id should be handled for districts if there's no direct relationship defined
            # If state_id in tbl_zone is meant to reference a state in the state table, this approach is valid
            # If not, and districts are independent, you might omit state_id or handle it differently
            pg_cursor.execute("""
                INSERT INTO district (id, name, state_id)
                VALUES (%s, %s, NULL)  -- Assuming state_id is not applicable; adjust as necessary
                ON CONFLICT (name) DO NOTHING
            """, (row['id'], row['name']))

    pg_conn.commit()

    print("State and district tables created and populated successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close connections
    if mysql_conn:
        mysql_conn.close()
    if pg_conn:
        pg_conn.close()
