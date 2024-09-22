CREATE OR REPLACE PROCEDURE raw.imported_leave_information_archive()
LANGUAGE SQL
AS $$
    UPDATE raw.imported_leave_information_archive
    SET is_overridden = TRUE
    WHERE ingested_at < NOW();

    INSERT INTO raw.imported_leave_information_archive
    SELECT * FROM raw.imported_leave_information;
$$;
