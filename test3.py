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

def get_id_from_name(pg_cursor, table, name):
    """Fetch the ID for a given name from the state or district table."""
    pg_cursor.execute(f"SELECT id FROM {table} WHERE name = %s", (name,))
    result = pg_cursor.fetchone()
    return result[0] if result else None

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

    # Migrate member data from MySQL tbl_member to PostgreSQL testuser based on state and district names
    with mysql_conn.cursor() as cursor:
        cursor.execute("""
            SELECT m.first_name, m.contact_number, p.name AS state_name, z.name AS district_name
            FROM tbl_member m
            JOIN tbl_province p ON m.state_id = p.id
            JOIN tbl_zone z ON m.district_id = z.id
        """)
        for row in cursor.fetchall():
            # Look up the state_id and district_id based on names
            state_id = get_id_from_name(pg_cursor, 'state', row['state_name'])
            district_id = get_id_from_name(pg_cursor, 'district', row['district_name'])

            if state_id and district_id:
                # Insert the member into testuser with the found state_id and district_id
                pg_cursor.execute("""
                    INSERT INTO testuser (name, mobile, state_id, district_id) 
                    VALUES (%s, %s, %s, %s)
                """, (row['first_name'], row['contact_number'], state_id, district_id))
            else:
                print(f"Skipping member {row['first_name']} due to missing state or district")

        pg_conn.commit()

    print("Member data migration completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure connections are closed
    if mysql_conn:
        mysql_conn.close()
    if pg_conn:
        pg_conn.close()
