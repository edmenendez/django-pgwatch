# Django PGWatch Example Project

This is a minimal Django project demonstrating how to use the `django_pgwatch` package.

## Quick Start

1. **Start PostgreSQL:**
   ```bash
   docker-compose up -d
   ```

2. **Install dependencies:**
   ```bash
   pip install django psycopg
   pip install -e ..  # Install django_pgwatch from parent directory
   ```

3. **Set up the database:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Create some database triggers** (optional):
   ```bash
   python manage.py shell
   ```
   
   ```python
   from django_pgwatch.utils import smart_notify
   from django.db import connection
   
   # Create a trigger on the auth_user table
   with connection.cursor() as cursor:
       cursor.execute('''
       CREATE TRIGGER notify_user_changes
           AFTER INSERT OR UPDATE OR DELETE ON auth_user
           FOR EACH ROW EXECUTE FUNCTION notify_data_change();
       ''')
   ```

5. **Run the Django server:**
   ```bash
   python manage.py runserver
   ```

6. **In another terminal, start the consumer:**
   ```bash
   python manage.py pgwatch_listen
   ```

## Testing the System

### Send a Manual Notification

```python
python manage.py shell
```

```python
from django_pgwatch.utils import smart_notify

# Send a test notification
smart_notify('data_change', {
    'event': 'test',
    'message': 'Hello from django_pgwatch!'
})
```

### Create/Edit Users

1. Go to http://localhost:8000/admin/
2. Log in with your superuser account
3. Create, edit, or delete users
4. Watch the console running `pgwatch_listen` for notifications

### Custom Notifications

```python
# Send custom events
smart_notify('user_events', {
    'event_type': 'login',
    'user_id': 123,
    'timestamp': '2025-01-01T12:00:00Z'
})

smart_notify('system_alerts', {
    'alert_type': 'high_cpu',
    'severity': 'warning',
    'value': 85.6
})
```

## Example Consumer Output

When you make changes to users, you'll see output like:

```
📋 Notification received: Notification 123 on data_change (real-time)
   Channel: data_change
   Data: {'table': 'auth_user', 'action': 'INSERT', 'id': 1, ...}
   Replay: False
   📊 Database Change:
      Table: auth_user
      Action: INSERT  
      Record ID: 1

🆕 New user created: john_doe
   📨 Sending welcome email to john@example.com

🗄️ Invalidating cache for auth_user:1
   ❌ Clearing cache key: auth_user:1
   ❌ Clearing cache key: auth_user:list
   ❌ Clearing cache key: stats:auth_user

📈 Analytics: {'event_type': 'database_change', 'table': 'auth_user', ...}
```

## Available Consumers

The example includes several consumer patterns:

- **LoggingConsumer**: Logs all notifications for debugging
- **UserChangeConsumer**: Handles user-specific events  
- **CacheInvalidationConsumer**: Invalidates cache on data changes
- **AnalyticsConsumer**: Tracks events for analytics
- **MultiChannelConsumer**: Routes notifications by channel

## Management Commands

```bash
# List available consumers
python manage.py pgwatch_listen --list-consumers

# Run specific consumers only
python manage.py pgwatch_listen --consumers logging_consumer user_change_consumer

# Run with custom settings
python manage.py pgwatch_listen --timeout=60 --max-batch-size=50
```

## Environment Variables

- `POSTGRES_DB`: Database name (default: pgwatch_example)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_HOST`: Database host (default: localhost)
- `POSTGRES_PORT`: Database port (default: 5432)