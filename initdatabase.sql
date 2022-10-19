SELECT 'CREATE DATABASE printjobs'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'printjobs');\gexec

\c printjobs
