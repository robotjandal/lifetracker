INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO goals (title, author_id, created)
VALUES
  ('First test goal', 1, '2018-01-01 00:00:00'),
  ('Second test goal', 1, '2018-01-02 00:00:00');


INSERT INTO progress (progress, goal_id, author_id, created)
VALUES
-- Introducing five progress points for the first goal (five days)
  (5, 1, 1, '2018-01-01 00:00:00'),
  (3, 1, 1, '2018-01-02 00:00:00'),
  (5, 1, 1, '2018-01-03 00:01:00'),
  (5, 1, 1, '2018-01-04 00:00:00'),
  (3, 1, 1, '2018-01-05 00:00:00'),  
  (5, 1, 1, '2018-01-06 00:00:00'),  
-- Introducing six progress points for the second goal (five days)
  (5, 2, 1, '2018-01-01 00:00:00'),
  (3, 2, 1, '2018-01-02 00:00:00'),
  (3, 2, 1, '2018-01-03 00:00:00'),
  (3, 2, 1, '2018-01-04 00:00:00'),
  (4, 2, 1, '2018-01-04 00:01:00'),
  (5, 2, 1, '2018-01-05 00:01:00'),
  (5, 2, 1, '2018-01-06 00:01:00');
