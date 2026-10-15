
```javascript
// Step 2: Switch to the bookstore database
db = db.getSiblingDB("bookstore");

// Step 3: Load authors.json
db.authors.drop();
var authors = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(authors);

// Step 4: Load books.json
db.books.drop();
var books = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(books);

// Step 5: List all authors and books
print("All Authors:");
db.authors.find().forEach(printjson);

print("All Books:");
db.books.find().forEach(printjson);

// Step 6: Insert two new books
db.books.insertMany([
  {
    title: "Harry Potter and the Sorcerer's Stone",
    published_year: 1997,
    author_ids: ["author_004"]
  },
  {
    title: "Harry Potter and the Chamber of Secrets",
    published_year: 1998,
    author_ids: ["author_004"]
  }
]);

// Step 7: Add the missing author
db.authors.insertOne({
  _id: "author_004",
  name: "J.K. Rowling",
  nationality: "British",
  bio: {
    short: "British author known for the Harry Potter series.",
    long: "J.K. Rowling is a British novelist best known for writing the Harry Potter fantasy book series."
  }
});

// Step 8: Filter books by a list of authors
print("Books by selected authors:");
db.books.find({
  author_ids: {
    $in: ["author_001", "author_004"]
  }
}).forEach(printjson);
```
