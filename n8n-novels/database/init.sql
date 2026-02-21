-- ===========================================
-- N8N NOVEL WRITING SYSTEM - DATABASE SCHEMA
-- ===========================================
-- This file initializes the database for the n8n novel writing system
-- It will be automatically run when the PostgreSQL container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===========================================
-- PROJECTS TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    subgenre VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active',
    ai_model VARCHAR(50) NOT NULL,
    backup_ai_model VARCHAR(50),
    target_chapters INTEGER DEFAULT 20,
    current_chapter INTEGER DEFAULT 0,
    words_per_chapter_min INTEGER DEFAULT 3000,
    words_per_chapter_target INTEGER DEFAULT 4000,
    words_per_chapter_max INTEGER DEFAULT 6000,
    quality_threshold_approve INTEGER DEFAULT 75,
    quality_threshold_review INTEGER DEFAULT 70,
    quality_threshold_regenerate INTEGER DEFAULT 60,
    schedule_frequency VARCHAR(50) DEFAULT 'daily',
    schedule_time TIME DEFAULT '09:00:00',
    price_per_chapter DECIMAL(10,2),
    target_platform TEXT[],
    tags TEXT[],
    description TEXT,
    cover_image_path VARCHAR(500),
    config_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- ===========================================
-- CHARACTERS TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    character_id VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL, -- protagonist, antagonist, supporting, minor
    age INTEGER,
    gender VARCHAR(50),
    personality TEXT[],
    background TEXT,
    motivation TEXT,
    appearance TEXT,
    speech_pattern TEXT,
    relationships JSONB,
    abilities JSONB,
    character_arc TEXT,
    full_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, character_id)
);

-- ===========================================
-- CHAPTERS TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS chapters (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    chapter_number INTEGER NOT NULL,
    title VARCHAR(500),
    word_count INTEGER,
    ai_model VARCHAR(50),
    status VARCHAR(50) DEFAULT 'draft', -- draft, qc_pending, approved, published, flagged
    outline TEXT,
    summary TEXT,
    key_events TEXT[],
    characters_involved TEXT[],
    filepath VARCHAR(500),
    generation_attempts INTEGER DEFAULT 1,
    generation_cost_usd DECIMAL(10,4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(project_id, chapter_number)
);

-- ===========================================
-- QUALITY SCORES TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS quality_scores (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    qc_layer VARCHAR(50) NOT NULL, -- basic, ai_scorer, deep_check, expert, human
    overall_score INTEGER,
    grammar_score INTEGER,
    character_score INTEGER,
    plot_score INTEGER,
    emotion_score INTEGER,
    genre_score INTEGER,
    pacing_score INTEGER,
    dialogue_score INTEGER,
    issues JSONB,
    suggestions JSONB,
    verdict VARCHAR(50), -- approve, review, regenerate, flag
    reviewer VARCHAR(100), -- AI model name or 'human'
    review_cost_usd DECIMAL(10,4),
    reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- EXECUTION LOGS TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS execution_logs (
    id SERIAL PRIMARY KEY,
    workflow_name VARCHAR(200) NOT NULL,
    workflow_id VARCHAR(100),
    project_id VARCHAR(100),
    chapter_number INTEGER,
    status VARCHAR(50) NOT NULL, -- started, success, failed, partial
    duration_seconds INTEGER,
    api_calls INTEGER,
    api_cost_usd DECIMAL(10,4),
    input_tokens INTEGER,
    output_tokens INTEGER,
    error_message TEXT,
    details JSONB,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- OUTLINES TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS outlines (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    outline_type VARCHAR(50) NOT NULL, -- master, arc, chapter
    arc_number INTEGER,
    chapter_number INTEGER,
    content TEXT NOT NULL,
    structure JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- WORLD BUILDING TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS world_building (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL, -- magic_system, geography, politics, culture, history
    name VARCHAR(200) NOT NULL,
    description TEXT,
    rules TEXT[],
    data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, category, name)
);

-- ===========================================
-- TIMELINE TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS timeline_events (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    chapter_number INTEGER,
    event_order INTEGER,
    event_date VARCHAR(100), -- in-story date
    event_time VARCHAR(100), -- in-story time
    description TEXT NOT NULL,
    characters_involved TEXT[],
    location VARCHAR(200),
    importance VARCHAR(50), -- major, minor, background
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- API USAGE TRACKING TABLE
-- ===========================================
CREATE TABLE IF NOT EXISTS api_usage (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    ai_provider VARCHAR(50) NOT NULL, -- anthropic, openai, google
    model VARCHAR(100) NOT NULL,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    total_cost_usd DECIMAL(10,4) DEFAULT 0,
    request_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, ai_provider, model)
);

-- ===========================================
-- INDEXES
-- ===========================================
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_genre ON projects(genre);
CREATE INDEX IF NOT EXISTS idx_chapters_project ON chapters(project_id);
CREATE INDEX IF NOT EXISTS idx_chapters_status ON chapters(status);
CREATE INDEX IF NOT EXISTS idx_quality_scores_chapter ON quality_scores(chapter_id);
CREATE INDEX IF NOT EXISTS idx_execution_logs_project ON execution_logs(project_id);
CREATE INDEX IF NOT EXISTS idx_execution_logs_date ON execution_logs(executed_at);
CREATE INDEX IF NOT EXISTS idx_characters_project ON characters(project_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_date ON api_usage(date);

-- ===========================================
-- UPDATE TIMESTAMP TRIGGER
-- ===========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables with updated_at
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_characters_updated_at BEFORE UPDATE ON characters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chapters_updated_at BEFORE UPDATE ON chapters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_outlines_updated_at BEFORE UPDATE ON outlines
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_world_building_updated_at BEFORE UPDATE ON world_building
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_api_usage_updated_at BEFORE UPDATE ON api_usage
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ===========================================
-- VIEWS
-- ===========================================

-- Project summary view
CREATE OR REPLACE VIEW project_summary AS
SELECT
    p.project_id,
    p.title,
    p.genre,
    p.status,
    p.ai_model,
    p.target_chapters,
    p.current_chapter,
    COUNT(DISTINCT c.id) as total_chapters,
    COALESCE(SUM(c.word_count), 0) as total_words,
    COALESCE(AVG(qs.overall_score), 0) as avg_quality_score,
    COALESCE(SUM(c.generation_cost_usd), 0) as total_generation_cost,
    p.created_at,
    p.updated_at
FROM projects p
LEFT JOIN chapters c ON p.project_id = c.project_id
LEFT JOIN quality_scores qs ON c.id = qs.chapter_id AND qs.qc_layer = 'deep_check'
GROUP BY p.id;

-- Daily stats view
CREATE OR REPLACE VIEW daily_stats AS
SELECT
    DATE(executed_at) as date,
    COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_runs,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_runs,
    SUM(api_cost_usd) as total_cost,
    SUM(input_tokens) as total_input_tokens,
    SUM(output_tokens) as total_output_tokens
FROM execution_logs
GROUP BY DATE(executed_at)
ORDER BY date DESC;

-- ===========================================
-- SAMPLE DATA (Optional - comment out in production)
-- ===========================================
-- INSERT INTO projects (project_id, title, genre, ai_model, target_chapters)
-- VALUES ('sample-001', 'Sample Project', 'fantasy', 'gemini', 20);

COMMENT ON DATABASE n8n_novels IS 'Database for n8n Novel Writing Automation System';
