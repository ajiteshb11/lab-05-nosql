
#!/usr/bin/env python3
"""Generate a bookstore inventory report using MongoDB Atlas."""

import logging
import os

from pymongo import MongoClient

# Read database credentials from environment variables.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def main():
    """Connect to MongoDB and report books for selected authors."""
    client = None

    try:
        # Check that credentials are available.
        if not all([
            MONGODB_ATLAS_URL,
            MONGODB_ATLAS_USER,
            MONGODB_ATLAS_PWD
        ]):
            raise ValueError(
                "Missing MongoDB environment variables."
            )

        # Connect to MongoDB Atlas.
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000
        )

        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas successfully.")

        # Select the bookstore database and collections.
        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        # Include authors from the original data and a new author.
        author_ids = [
            "author_001",
            "author_002",
            "author_003",
            "author_004"
        ]

        # Count the selected authors.
        author_count = authors.count_documents({
            "_id": {"$in": author_ids}
        })

        print(f"\nAuthors: {author_count}\n")

        # Find each author and their associated books.
        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})

            if author is None:
                logging.warning(
                    "Author %s was not found.",
                    author_id
                )
                continue

            print(author["name"])

            # Find books that reference this author's ID.
            author_books = books.find({
                "author_ids": author["_id"]
            })

            found_books = False

            for book in author_books:
                found_books = True
                title = book.get("title", "Unknown Title")
                year = book.get("published_year", "Unknown Year")

                print(f"  {title} ({year})")

            if not found_books:
                print("  No books found.")

            print()

    except Exception as error:
        logging.error("MongoDB report failed: %s", error)
        raise

    finally:
        # Always close the database connection.
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed.")


if __name__ == "__main__":
    main()
