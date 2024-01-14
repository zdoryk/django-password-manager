# your_django_app/sync_manager.py
from typing import List

from .cloud_db.mongo_client import MongoDBClient
from .models import PasswordEntry, SyncTimestamp
from django.db import transaction
from django.utils import timezone
from datetime import datetime


class SyncManager:
    def __init__(self, local_client, cloud_client):
        # self.local_client = local_client
        self.cloud_client = cloud_client

    def synchronize_data(self):
        try:
            # Connect to MongoDB
            self.cloud_client.connect()
            print("Connected\n")
            # Get new records from the cloud
            cloud_data = self.cloud_client.find_documents("PasswordsCollection")
            print(cloud_data)

            # SyncTimestamp.objects.create(last_sync=timezone.datetime(year=2024, month=1, day=1))

            # Synchronize data to SQLite
            self._synchronize_data_to_sqlite(cloud_data)

            # Synchronize data to MongoDB cloud
            self._synchronize_data_to_mongo_cloud(cloud_data)

        except Exception as e:
            print(f"Error during synchronization: {e}")

        finally:
            # Disconnect from MongoDB
            self.cloud_client.disconnect()

    @staticmethod
    def _synchronize_data_to_sqlite(cloud_data):
        with transaction.atomic():
            # Get existing records in SQLite
            local_records = PasswordEntry.objects.all()
            local_records_ids = [record.id for record in local_records]
            deleted_local_records_ids = [record.id for record in local_records.filter(is_deleted=True)]

            # Identify records to add (present in cloud but not in SQLite)
            records_to_add = [cloud_record for cloud_record in cloud_data if
                              cloud_record.get('id') not in local_records_ids]

            # Identify records to delete (present in SQLite but not in cloud)
            records_to_delete = [cloud_record for cloud_record in cloud_data if
                                 cloud_record.get('id') not in deleted_local_records_ids and cloud_record.get(
                                     'deleted_at')]

            print("\n\n")
            print(f"{records_to_add=}")
            print(f"{records_to_delete=}")
            # Add new records to SQLite
            for record_to_add in records_to_add:
                PasswordEntry.objects.create(
                    id=record_to_add.get('id'),
                    service=record_to_add.get('service'),
                    login=record_to_add.get('login'),
                    password=record_to_add.get('password'),
                    is_deleted=record_to_add.get('is_deleted'),
                    created_at=record_to_add.get('created_at'),
                    deleted_at=record_to_add.get('deleted_at'),
                )

            # Delete records from SQLite
            for record_to_delete in records_to_delete:
                # Set is_deleted to True and deleted_at to current timestamp
                PasswordEntry.objects.update_or_create(
                    id=record_to_delete.get('id'),
                    # service=record_to_delete.get('service'),
                    # login=record_to_delete.get('login'),
                    # password=record_to_delete.get('password'),
                    # created_at=record_to_delete.get('created_at'),
                    defaults={
                        'is_deleted': True,
                        'deleted_at': datetime.now(),
                    }
                )

    def _synchronize_data_to_mongo_cloud(self, cloud_data: List[dict]):

        new_created_records = PasswordEntry.objects.filter(created_at__gte=self.get_last_sync_timestamp(),
                                                           is_deleted=False)
        new_deleted_records = PasswordEntry.objects.filter(deleted_at__gte=self.get_last_sync_timestamp())

        not_deleted_cloud_records_ids: List[int] = [record.get('id') for record in cloud_data if
                                                    record.get('deleted_at') is None]
        deleted_cloud_records: List[int] = [record.get('id') for record in cloud_data if record.get('deleted_at')]

        records_to_add: List[PasswordEntry] = [record for record in new_created_records if
                                               record.id not in not_deleted_cloud_records_ids]
        records_to_delete: List[PasswordEntry] = [record for record in new_deleted_records if
                                                  record.id not in deleted_cloud_records]

        print(f"{records_to_add=}")
        print(f"{new_created_records=}")
        print(f"{records_to_delete=}")
        print(f"{new_deleted_records=}")

        for record in records_to_add:
            object_to_insert = record.__dict__
            object_to_insert.pop('_state')
            print(f"{object_to_insert=}")

            self.cloud_client.insert_document("PasswordsCollection", object_to_insert)

        for record in records_to_delete:
            update_document = record.__dict__.copy()
            update_document.pop('_state')
            update_document['is_deleted'] = True
            update_document['deleted_at'] = datetime.now()
            self.cloud_client.set_record_deleted(collection="PasswordsCollection",
                                                 query={"id": record.id},
                                                 update_document=update_document)

    @staticmethod
    def get_last_sync_timestamp():
        # Replace this with your actual logic to retrieve the last synchronization timestamp from your storage
        # For example, you can store it in a settings file, database, or any other persistent storage
        return SyncTimestamp.objects.last().last_sync
