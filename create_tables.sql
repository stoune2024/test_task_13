-- ================================
-- 1️⃣  СОЗДАНИЕ БАЗЫ ДАННЫХ
-- ================================

-- ⚠️ Важно:
-- Этот блок нужно выполнять от имени пользователя с правом создания БД (например, postgres)
-- Если база уже существует, следующая команда может завершиться ошибкой — это нормально.

CREATE DATABASE video_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TEMPLATE = template0;

-- ================================
-- 2️⃣  ПОДКЛЮЧЕНИЕ К НОВОЙ БАЗЕ
-- ================================
\connect video_db;

-- ================================
-- 3️⃣  СОЗДАНИЕ ТАБЛИЦ
-- ================================

CREATE TABLE IF NOT EXISTS video_analysis (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS violations (
    id SERIAL PRIMARY KEY,
    analysis_id INTEGER REFERENCES video_analysis(id) ON DELETE CASCADE,
    frame INTEGER,
    type VARCHAR,
    confidence FLOAT
);

-- ================================
-- 4️⃣  ДОПОЛНИТЕЛЬНО (опционально)
-- ================================

-- Индексы для ускорения выборок
CREATE INDEX IF NOT EXISTS idx_violations_analysis_id ON violations (analysis_id);
CREATE INDEX IF NOT EXISTS idx_video_analysis_created_at ON video_analysis (created_at);

-- Проверим, что всё успешно создано
\dt
