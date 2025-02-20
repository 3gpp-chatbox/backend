CREATE EXTENSION IF NOT EXISTS ltree;

CREATE TABLE documents (
  doc_id SERIAL PRIMARY KEY,
  doc_name TEXT NOT NULL,
  extracted_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sections (
  section_id SERIAL PRIMARY KEY,
  doc_id INT REFERENCES documents(doc_id) ON DELETE CASCADE,
  heading TEXT NOT NULL,
  level INT NOT NULL,
  content TEXT NOT NULL,
  parent TEXT NOT NULL,
  path LTREE NOT NULL  -- e.g., 'TopSection.SubSection'
);

CREATE INDEX idx_sections_path ON sections USING GIST (path);