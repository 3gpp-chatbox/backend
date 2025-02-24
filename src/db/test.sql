SELECT section_id, heading, level, parent, path, content
FROM sections
WHERE doc_id = 1
ORDER BY path;


-- Query recursively
SELECT section_id, heading, level, parent, path, content
FROM sections
WHERE path <@ '4_general'
AND doc_id = 1
ORDER BY path;


SELECT section_id, heading, level, parent, path, content
FROM sections
WHERE path ~ '4_general.*{1,}'
AND doc_id = 1
AND level = 2
ORDER BY heading;




