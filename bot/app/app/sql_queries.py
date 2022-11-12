"""Module with SQL Queries."""

SELECT_RANDOM_WORD_PAIR = """
SELECT 
    data.word, 
    data.word_representation,
    data.translation,
    data.translation_representation
FROM 
(
    SELECT 
        word, 
        word_representation,
        translation,
        translation_representation
    FROM user_translation 
    WHERE user_id = :user_id
UNION 
    SELECT
        dictionary_content.word,
        dictionary_content.word as word_representation,
        dictionary_content.translation,
        dictionary_content.translation as translation_representation
    FROM
    (
        SELECT
            user_id,
            dictionary_id
        FROM users_dictionaries WHERE user_id = :user_id
    ) AS u_d
    INNER JOIN dictionary_content
        ON u_d.dictionary_id = dictionary_content.dictionary_id
    
) AS data
ORDER BY random() 
LIMIT 1;"""
