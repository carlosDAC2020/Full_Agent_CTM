-- Create separate databases for Magazine and Agent apps
CREATE DATABASE mag_db;
CREATE DATABASE agent_db;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mag_db TO shared_user;
GRANT ALL PRIVILEGES ON DATABASE agent_db TO shared_user;
