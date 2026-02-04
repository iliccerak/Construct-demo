BEGIN;

ALTER TABLE refresh_tokens
    ADD COLUMN IF NOT EXISTS jti TEXT;

UPDATE refresh_tokens SET jti = id::text WHERE jti IS NULL;

ALTER TABLE refresh_tokens
    ALTER COLUMN jti SET NOT NULL;

DO $$ BEGIN
    ALTER TABLE refresh_tokens
        ADD CONSTRAINT refresh_tokens_jti_unique UNIQUE (jti);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

COMMIT;
