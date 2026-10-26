# Database Migrations (Alembic)

Use Alembic to manage database revisions:
```bash
# Generate revision
alembic revision --autogenerate -m "create initial tables"

# Upgrade database
alembic upgrade head
```
