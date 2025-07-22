# read_firestore.py
from .firestore_connector import db


def print_firestore_data(collection_name: str):
    docs = db.collection(collection_name).stream()
    print(f"\n📄 Documents in '{collection_name}':")
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")

if __name__ == "__main__":
    print_firestore_data("lessons")
