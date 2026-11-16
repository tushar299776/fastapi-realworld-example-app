-- name: add-article-to-bookmarks!
INSERT INTO bookmarks (user_id, article_id)
VALUES ((SELECT id FROM users WHERE username = :username),
        (SELECT id FROM articles WHERE slug = :slug))
ON CONFLICT DO NOTHING;


-- name: remove-article-from-bookmarks!
DELETE
FROM bookmarks
WHERE user_id = (SELECT id FROM users WHERE username = :username)
  AND article_id = (SELECT id FROM articles WHERE slug = :slug);


-- name: is-article-bookmarked^
SELECT CASE WHEN count(user_id) > 0 THEN TRUE ELSE FALSE END AS bookmarked
FROM bookmarks
WHERE user_id = (SELECT id FROM users WHERE username = :username)
  AND article_id = (SELECT id FROM articles WHERE slug = :slug);


-- name: get-bookmarks-for-user
SELECT a.id,
       a.slug,
       a.title,
       a.description,
       a.body,
       a.created_at,
       a.updated_at,
       (SELECT username FROM users WHERE id = a.author_id) AS author_username
FROM articles a
INNER JOIN bookmarks b ON a.id = b.article_id
WHERE b.user_id = (SELECT id FROM users WHERE username = :username)
ORDER BY b.user_id, a.id
LIMIT :limit
OFFSET :offset;
