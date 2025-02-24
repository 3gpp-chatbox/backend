INSERT INTO documents (doc_name) VALUES
  ('SampleDocument');


INSERT INTO sections (doc_id, heading, level, content, parent, path) VALUES
  (1, '1_intro', 1, 'Introduction to the document', NULL, '1_intro'),
  (1, '4_general', 1, 'General section content', NULL, '4_general'),
  (1, '4_general 1.1', 2, 'Subsection 1.1 content', '4_general', '4_general.4_general_1_1'),
  (1, '4_general 1.1.1', 3, 'Deep content under 1.1', '4_general 1.1', '4_general.4_general_1_1.4_general_1_1_1'),
  (1, '4_general 1.2', 2, 'Subsection 1.2 content', '4_general', '4_general.4_general_1_2'),
  (1, '4_general 1.2.1', 3, 'Deep content under 1.2', '4_general 1.2', '4_general.4_general_1_2.4_general_1_2_1'),
  (1, '5_other', 1, 'Another top-level section', NULL, '5_other');