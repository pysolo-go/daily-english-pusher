-- ChromaDB SQLite 查询示例

-- 1. 概览：查看所有向量切片及其对应的文档内容
-- ChromaDB 将元数据存储在 embedding_metadata 表中，通过 key-value 形式存储
-- 因此需要通过多次 JOIN 来将行转列，以便直观查看

SELECT 
    e.id AS internal_id,             -- 内部自增 ID
    e.embedding_id AS vector_uuid,   -- 向量的唯一 UUID
    m_doc.string_value AS content,   -- 切片文本内容 (key='chroma:document')
    m_file.string_value AS source,   -- 源文件名 (key='file_name')
    m_page.int_value AS page_num,    -- 页码 (key='page_label' 或 'page_idx'，视具体情况而定)
    e.created_at                     -- 创建时间
FROM 
    embeddings e
-- 关联文档内容
LEFT JOIN 
    embedding_metadata m_doc 
    ON e.id = m_doc.id AND m_doc.key = 'chroma:document'
-- 关联源文件名
LEFT JOIN 
    embedding_metadata m_file 
    ON e.id = m_file.id AND m_file.key = 'file_name'
-- 关联页码 (如果有的话，通常是 page_label)
LEFT JOIN 
    embedding_metadata m_page 
    ON e.id = m_page.id AND m_page.key = 'page_label'
ORDER BY 
    e.id ASC;

-- 2. 统计：查看每个文件的切片数量
SELECT 
    m.string_value AS file_name,
    COUNT(*) AS chunk_count
FROM 
    embeddings e
JOIN 
    embedding_metadata m 
    ON e.id = m.id AND m.key = 'file_name'
GROUP BY 
    m.string_value
ORDER BY 
    chunk_count DESC;

-- 3. 查看系统表：列出所有 Collection
SELECT * FROM collections;
