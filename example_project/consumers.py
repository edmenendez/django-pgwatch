"""
Example consumers demonstrating django_pgwatch usage.

These consumers show different patterns for handling PostgreSQL notifications.
"""

from django_pgwatch.consumer import BaseConsumer


class LoggingConsumer(BaseConsumer):
    """
    Simple consumer that logs all notifications to the console.
    Useful for debugging and monitoring.
    """
    consumer_id = 'logging_consumer'
    channels = ['data_change']
    
    def handle_notification(self, handler):
        print(f"📋 Notification received: {handler}")
        print(f"   Channel: {handler.channel}")
        print(f"   Data: {handler.data}")
        print(f"   Replay: {handler.is_replay}")
        
        if handler.is_database_change():
            print(f"   📊 Database Change:")
            print(f"      Table: {handler.get_table()}")
            print(f"      Action: {handler.get_action()}")
            print(f"      Record ID: {handler.get_record_id()}")


class UserChangeConsumer(BaseConsumer):
    """
    Consumer that specifically handles user table changes.
    Demonstrates filtering and specialized processing.
    """
    consumer_id = 'user_change_consumer'
    channels = ['data_change']
    
    def handle_notification(self, handler):
        # Only process user table changes
        if handler.get_table() != 'auth_user':
            return
            
        action = handler.get_action()
        user_data = handler.get_new_data() or handler.get_old_data()
        
        if action == 'INSERT':
            print(f"🆕 New user created: {user_data.get('username')}")
            self.send_welcome_email(user_data)
            
        elif action == 'UPDATE':
            old_data = handler.get_old_data()
            new_data = handler.get_new_data()
            
            if old_data.get('email') != new_data.get('email'):
                print(f"📧 Email changed for {new_data.get('username')}")
                
        elif action == 'DELETE':
            print(f"🗑️ User deleted: {user_data.get('username')}")
    
    def send_welcome_email(self, user_data):
        """Simulate sending a welcome email"""
        print(f"   📨 Sending welcome email to {user_data.get('email')}")


class CacheInvalidationConsumer(BaseConsumer):
    """
    Consumer that invalidates cache entries when data changes.
    Common pattern for maintaining cache consistency.
    """
    consumer_id = 'cache_invalidation_consumer' 
    channels = ['data_change']
    
    def handle_notification(self, handler):
        if not handler.is_database_change():
            return
            
        table = handler.get_table()
        record_id = handler.get_record_id()
        
        # Generate cache keys to invalidate
        cache_keys = [
            f"{table}:{record_id}",
            f"{table}:list",
            f"stats:{table}",
        ]
        
        print(f"🗄️ Invalidating cache for {table}:{record_id}")
        for key in cache_keys:
            print(f"   ❌ Clearing cache key: {key}")
            # In real implementation: cache.delete(key)


class AnalyticsConsumer(BaseConsumer):
    """
    Consumer that tracks events for analytics.
    Demonstrates async processing and error handling.
    """
    consumer_id = 'analytics_consumer'
    channels = ['data_change', 'user_events']
    
    def handle_notification(self, handler):
        try:
            if handler.channel == 'data_change':
                self.track_database_change(handler)
            elif handler.channel == 'user_events':
                self.track_user_event(handler)
                
        except Exception as e:
            print(f"❌ Analytics tracking failed: {e}")
            # Don't re-raise - we don't want to block other consumers
    
    def track_database_change(self, handler):
        """Track database changes"""
        event_data = {
            'event_type': 'database_change',
            'table': handler.get_table(),
            'action': handler.get_action(),
            'record_id': handler.get_record_id(),
            'timestamp': handler.timestamp,
        }
        print(f"📈 Analytics: {event_data}")
    
    def track_user_event(self, handler):
        """Track custom user events"""
        event_data = handler.data
        print(f"👤 User Event: {event_data}")


class MultiChannelConsumer(BaseConsumer):
    """
    Consumer that listens to multiple channels and routes accordingly.
    """
    consumer_id = 'multi_channel_consumer'
    channels = ['data_change', 'user_events', 'system_alerts']
    
    def handle_notification(self, handler):
        if handler.channel == 'data_change':
            self.handle_data_change(handler)
        elif handler.channel == 'user_events':
            self.handle_user_event(handler)
        elif handler.channel == 'system_alerts':
            self.handle_system_alert(handler)
    
    def handle_data_change(self, handler):
        print(f"🔄 Data change: {handler.get_table()} {handler.get_action()}")
    
    def handle_user_event(self, handler):
        print(f"👤 User event: {handler.data}")
    
    def handle_system_alert(self, handler):
        print(f"🚨 System alert: {handler.data}")


# Example of dynamic consumer creation
def create_table_monitor(table_name):
    """
    Factory function to create a consumer that monitors a specific table.
    """
    class TableMonitorConsumer(BaseConsumer):
        consumer_id = f'{table_name}_monitor'
        channels = ['data_change']
        
        def handle_notification(self, handler):
            if handler.get_table() == table_name:
                action = handler.get_action()
                record_id = handler.get_record_id()
                print(f"🔍 {table_name.title()} {action}: ID {record_id}")
    
    return TableMonitorConsumer