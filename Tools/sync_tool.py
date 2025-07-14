from typing import Dict, Any
from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger

logger = get_logger(__name__)

class SyncTool:
    """
    Synchronizes lesson, quiz, and progress data between Firestore and IndexedDB.
    Supports offline-first education architecture.
    """

    def __init__(self, firestore_client, indexeddb_client):
        self.firestore = firestore_client
        self.indexeddb = indexeddb_client

    @retry_with_backoff(retries=3, delay=2)
    def sync_from_firestore(self, student_id: str) -> Dict[str, Any]:
        try:
            data = self.firestore.get_document(student_id)
            self.indexeddb.save_document(student_id, data)
            logger.info(f"✅ Synced Firestore ➝ IndexedDB for {student_id}")
            return {"status": "success", "source": "firestore", "synced_data": data}
        except Exception as e:
            logger.exception("❌ Firestore sync failed")
            return {"status": "error", "error": str(e)}

    @retry_with_backoff(retries=3, delay=2)
    def sync_to_firestore(self, student_id: str) -> Dict[str, Any]:
        try:
            data = self.indexeddb.get_document(student_id)
            self.firestore.update_document(student_id, data)
            logger.info(f"✅ Synced IndexedDB ➝ Firestore for {student_id}")
            return {"status": "success", "source": "indexeddb", "synced_data": data}
        except Exception as e:
            logger.exception("❌ IndexedDB sync failed")
            return {"status": "error", "error": str(e)}
