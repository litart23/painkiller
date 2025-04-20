-- t_users

-- 1. Создание записи в базе (Create)
INSERT INTO t_users (name, login, password)
VALUES ('Имя пользователя', 'логин', 'пароль');


-- 2. Удаление записи из базы (Delete)
-- Удаление по ID
DELETE FROM t_users WHERE id = 1;

-- Или удаление по логину
DELETE FROM t_users WHERE login = 'логин';


-- 3. Обновление поля name (Update)
-- Обновление по ID
UPDATE t_users SET name = 'Новое имя' WHERE id = 1;

-- Или обновление по логину
UPDATE t_users SET name = 'Новое имя' WHERE login = 'логин';


-- 4. Обновление поля password (Update)
-- Обновление по ID
UPDATE t_users SET password = 'новый_пароль' WHERE id = 1;

-- Или обновление по логину
UPDATE t_users SET password = 'новый_пароль' WHERE login = 'логин';


-- t_issue

-- 1. Создание записи в базе (Create)
INSERT INTO t_issue (user_id, created, title, description, id_tag, active, resolved, repeated)
VALUES (1, CURRENT_DATE, 'Название проблемы', 'Описание проблемы', 5, TRUE, FALSE, 0);


-- 2. Удаление записи из базы (Delete)
-- Удаление по ID
DELETE FROM t_issue WHERE id = 1;

-- Удаление всех неактивных записей
DELETE FROM t_issue WHERE active = FALSE;


-- 3. Обновление полей title и description (Update)
-- Обновление по ID
UPDATE t_issue 
SET title = 'Новое название', description = 'Новое описание'
WHERE id = 1;

-- Обновление для всех активных записей конкретного пользователя
UPDATE t_issue
SET title = 'Обновленное название', description = 'Обновленное описание'
WHERE user_id = 5 AND active = TRUE;


-- 4. Обновление поля id_tag (Update)
-- Обновление тега по ID записи
UPDATE t_issue
SET id_tag = 7
WHERE id = 1;

-- Обновление тега для всех нерешенных проблем
UPDATE t_issue
SET id_tag = 3
WHERE resolved = FALSE;


-- 5. Изменение полей active и resolved (Update)
-- Пометить как неактивную
UPDATE t_issue
SET active = FALSE
WHERE id = 1;

-- Пометить как решенную
UPDATE t_issue
SET resolved = TRUE
WHERE id = 1;

-- Пакетное обновление: закрыть все решенные задачи
UPDATE t_issue
SET active = FALSE
WHERE resolved = TRUE;


-- 6. Увеличение счетчика repeated (Update)
-- Увеличить счетчик на 1 для конкретной записи
UPDATE t_issue
SET repeated = repeated + 1
WHERE id = 1;

-- Увеличить счетчик для всех активных повторяющихся проблем
UPDATE t_issue
SET repeated = repeated + 1
WHERE active = TRUE AND resolved = FALSE;