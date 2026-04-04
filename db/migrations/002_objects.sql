CREATE TABLE musicians_log (
    id SERIAL PRIMARY KEY,
    musician_id INT,
    action VARCHAR(16) NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE VIEW v_concerts_with_count AS
SELECT c.id, c.title, c.concert_date, c.venue, c.city,
       COUNT(p.id) AS musicians_count
FROM concerts c
LEFT JOIN performances p ON p.concert_id = c.id
GROUP BY c.id;

CREATE VIEW v_musicians_with_instruments AS
SELECT m.id, m.name, m.country, m.birth_year,
       STRING_AGG(DISTINCT i.name, ', ' ORDER BY i.name) AS instruments
FROM musicians m
LEFT JOIN performances p ON p.musician_id = m.id
LEFT JOIN instruments i ON i.id = p.instrument_id
GROUP BY m.id;

CREATE VIEW v_top_musicians AS
SELECT m.id, m.name, COUNT(p.id) AS performances_count
FROM musicians m
LEFT JOIN performances p ON p.musician_id = m.id
GROUP BY m.id
ORDER BY performances_count DESC;

CREATE FUNCTION fn_musician_age(p_birth_year INT)
RETURNS INT
LANGUAGE plpgsql AS $$
BEGIN
    IF p_birth_year IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN EXTRACT(YEAR FROM CURRENT_DATE)::INT - p_birth_year;
END;
$$;

CREATE FUNCTION fn_musician_total_fee(p_musician_id INT)
RETURNS NUMERIC
LANGUAGE plpgsql AS $$
DECLARE
    total NUMERIC;
BEGIN
    SELECT COALESCE(SUM(fee), 0) INTO total
    FROM performances
    WHERE musician_id = p_musician_id;
    RETURN total;
END;
$$;

CREATE FUNCTION fn_concerts_in_city(p_city VARCHAR)
RETURNS INT
LANGUAGE plpgsql AS $$
DECLARE
    cnt INT;
BEGIN
    SELECT COUNT(*) INTO cnt
    FROM concerts
    WHERE city = p_city;
    RETURN cnt;
END;
$$;

CREATE PROCEDURE sp_add_performance(
    p_musician_id INT,
    p_concert_id INT,
    p_instrument_id INT,
    p_fee NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM musicians WHERE id = p_musician_id) THEN
        RAISE EXCEPTION 'Musician with id % not found', p_musician_id;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM concerts WHERE id = p_concert_id) THEN
        RAISE EXCEPTION 'Concert with id % not found', p_concert_id;
    END IF;
    INSERT INTO performances (musician_id, concert_id, instrument_id, fee)
    VALUES (p_musician_id, p_concert_id, p_instrument_id, p_fee);
END;
$$;

CREATE PROCEDURE sp_delete_concert(p_concert_id INT)
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM concerts WHERE id = p_concert_id) THEN
        RAISE EXCEPTION 'Concert with id % not found', p_concert_id;
    END IF;
    DELETE FROM concerts WHERE id = p_concert_id;
END;
$$;

CREATE PROCEDURE sp_promote_user_to_admin(p_username VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE users SET role = 'admin' WHERE username = p_username;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'User % not found', p_username;
    END IF;
END;
$$;

CREATE FUNCTION trg_musicians_set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE FUNCTION trg_musicians_log_changes()
RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO musicians_log (musician_id, action) VALUES (NEW.id, 'INSERT');
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO musicians_log (musician_id, action) VALUES (NEW.id, 'UPDATE');
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO musicians_log (musician_id, action) VALUES (OLD.id, 'DELETE');
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$;

CREATE FUNCTION trg_check_birth_year()
RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.birth_year IS NOT NULL AND
       (NEW.birth_year < 1900 OR NEW.birth_year > EXTRACT(YEAR FROM CURRENT_DATE)::INT) THEN
        RAISE EXCEPTION 'Invalid birth year: %', NEW.birth_year;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_set_updated_at
BEFORE UPDATE ON musicians
FOR EACH ROW EXECUTE FUNCTION trg_musicians_set_updated_at();

CREATE TRIGGER trg_log_musicians
AFTER INSERT OR UPDATE OR DELETE ON musicians
FOR EACH ROW EXECUTE FUNCTION trg_musicians_log_changes();

CREATE TRIGGER trg_validate_birth_year
BEFORE INSERT OR UPDATE ON musicians
FOR EACH ROW EXECUTE FUNCTION trg_check_birth_year();
