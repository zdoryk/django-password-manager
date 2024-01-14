# your_django_app/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .sync_manager import SyncManager


@receiver(post_migrate)
def synchronize_data(sender, **kwargs):
    from .cloud_db.mongo_client import MongoDBClient
    print("Synchronizing data...")
    # Initialize MongoDB client for the cloud database
    cloud_mongo_client = MongoDBClient()

    # Initialize SyncManager
    sync_manager = SyncManager(None, cloud_mongo_client)

    # Perform synchronization logic
    sync_manager.synchronize_data()

