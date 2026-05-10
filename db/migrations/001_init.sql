CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(16) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE musicians (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    country VARCHAR(64),
    birth_year INT,
    bio TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE instruments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
    kind VARCHAR(32)
);

CREATE TABLE concerts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    concert_date DATE NOT NULL,
    venue VARCHAR(128),
    city VARCHAR(64)
);

CREATE TABLE performances (
    id SERIAL PRIMARY KEY,
    musician_id INT NOT NULL REFERENCES musicians(id) ON DELETE CASCADE,
    concert_id INT NOT NULL REFERENCES concerts(id) ON DELETE CASCADE,
    instrument_id INT REFERENCES instruments(id) ON DELETE SET NULL,
    fee NUMERIC(10, 2),
    UNIQUE (musician_id, concert_id, instrument_id)
);
