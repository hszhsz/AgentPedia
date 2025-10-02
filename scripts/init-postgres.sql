-- PostgreSQL 初始化脚本
-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建数据库用户（如果需要）
-- CREATE USER agentpedia_user WITH PASSWORD 'agentpedia_password';
-- GRANT ALL PRIVILEGES ON DATABASE agentpedia TO agentpedia_user;
-- GRANT ALL ON SCHEMA public TO agentpedia_user;
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO agentpedia_user;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO agentpedia_user;