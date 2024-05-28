import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    "database": "gnt_test",
    "user": "admin",
    "host": "localhost"
}

# Connect to your PostgreSQL database
conn = psycopg2.connect(**db_params)
conn.autocommit = True
cur = conn.cursor()


# Create state and district tables
cur.execute("""
    CREATE TABLE IF NOT EXISTS state (
        state_id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    );
""")

# Recreate the district table with the unique constraint
cur.execute("""
CREATE TABLE district (
    district_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    state_id INTEGER NOT NULL,
    CONSTRAINT fk_state FOREIGN KEY(state_id) REFERENCES state(state_id),
    UNIQUE(name, state_id)
);
""")


# Populate state table
cur.execute("""
    INSERT INTO state (name)
    SELECT DISTINCT state FROM gnttest WHERE state IS NOT NULL
    ON CONFLICT (name) DO NOTHING;
""")

# Populate district table
cur.execute("""
    INSERT INTO district (name, state_id)
    SELECT DISTINCT u.district, s.state_id FROM gnttest u
    JOIN state s ON u.state = s.name
    WHERE u.district IS NOT NULL
    ON CONFLICT (name, state_id) DO NOTHING;
""")

# Alter user table to add foreign key columns
cur.execute("""
    ALTER TABLE gnttest
    ADD COLUMN IF NOT EXISTS state_id INTEGER,
    ADD COLUMN IF NOT EXISTS district_id INTEGER;
""")

# Update user table to set the foreign keys
cur.execute("""
    UPDATE gnttest u SET state_id = s.state_id FROM state s WHERE u.state = s.name;
""")

cur.execute("""
    UPDATE gnttest u SET district_id = d.district_id FROM district d WHERE u.district = d.name;
""")

# Add foreign key constraints to user table
constraint_commands = [
    """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint
            WHERE conname = 'fk_gnttest_state'
        ) THEN
            ALTER TABLE gnttest ADD CONSTRAINT fk_gnttest_state FOREIGN KEY (state_id) REFERENCES state(state_id);
        END IF;
    END
    $$;
    """,
    """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint
            WHERE conname = 'fk_gnttest_district'
        ) THEN
            ALTER TABLE gnttest ADD CONSTRAINT fk_gnttest_district FOREIGN KEY (district_id) REFERENCES district(district_id);
        END IF;
    END
    $$;
    """
]
for command in constraint_commands:
    cur.execute(command)

# Optionally, drop the original state and district columns from the user table
# WARNING: Make sure your application does not need these columns anymore before dropping them
# cur.execute("ALTER TABLE user DROP COLUMN state, DROP COLUMN district;")

# Clean up
cur.close()
conn.close()

print("Migration completed successfully.")
