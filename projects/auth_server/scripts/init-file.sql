-- dblink 설치
CREATE EXTENSION IF NOT EXISTS dblink;

--
DO $$
BEGIN
  -- 데이터베이스 존재 여부 확인
  IF NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'auth-server'
  )
  THEN
    -- 데이터베이스가 존재하지 않으면 생성
    PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE "auth-server"');
  END IF;
END
$$;

-- 테이블 생성
CREATE TABLE users (
	user_name VARCHAR NOT NULL,
	password VARCHAR,
	user_group VARCHAR,
	user_role VARCHAR,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
	PRIMARY KEY (user_name)
);