# ROADMAP

1. Add word input in quiz as `word/word`
2. Add documentation
3. Add weights for quiz
4. Modify quiz, send messages based on the weights
5. Add `EDIT TRANSLATION`
6. Add `LIST TRANSLATION`
7. Add internal `"urban dictionary""`

# Usage
1. Install docker & docker-compose
2. Create .env file with variables:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres
TELEGRAM_TOKEN="your telegram bot token"
```

3. Run `docker-compose up -d`
4. Interact with your bot!
