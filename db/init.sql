-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table with Together embeddings (768-dim)
CREATE TABLE IF NOT EXISTS user_documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR NOT NULL,
    content TEXT,
    content_vector VECTOR(768)
);

-- ANN index for cosine similarity
CREATE INDEX IF NOT EXISTS idx_user_documents_vec_cos
ON user_documents USING ivfflat (content_vector vector_cosine_ops) WITH (lists = 100);
