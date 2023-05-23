const express = require("express");
const cors = require("cors");
const mongodb = require("mongodb");
const { MongoClient } = mongodb;

// Create a new Express app
const app = express();

// Enable Cross-Origin Resource Sharing
app.use(cors());
app.use(express.json());

// MongoDB connection URI
const uri ="mongodb+srv://krishna:book@cluster0.nsbsrbo.mongodb.net/?retryWrites=true&w=majority"
//   "mongodb+srv://krishna:book@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority";
const dbName = "ads9";
const collectionName = "customers";

// Create MongoDB client
const client = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Connect to the MongoDB server
client.connect((err) => {
  if (err) {
    throw err;
  }
  console.log("Connected to MongoDB server...");
});

// Create a new record
app.post("/data", (req, res) => {
  const { name, id, email } = req.body;
  const collection = client.db(dbName).collection(collectionName);

  collection
    .insertOne({ name, id, email })
    .then((result) => {
      res.json({
        message: "Record created successfully",
        id: result.insertedId,
      });
    })
    .catch((err) => {
      console.error(err);
      res.status(500).json({ message: "Failed to create record" });
    });
});

// Read all records
app.get("/data", (req, res) => {
  const collection = client.db(dbName).collection(collectionName);

  collection
    .find()
    .toArray()
    .then((result) => {
      res.json(result);
    })
    .catch((err) => {
      console.error(err);
      res.status(500).json({ message: "Failed to fetch records" });
    });
});

// Read a single record
app.get("/data/:id", (req, res) => {
  const { id } = req.params;
  const collection = client.db(dbName).collection(collectionName);

  collection
    .findOne({ _id: (id) })
    .then((result) => {
      if (!result) {
        return res.status(404).json({ message: "Record not found" });
      }
      res.json(result);
    })
    .catch((err) => {
      console.error(err);
      res.status(500).json({ message: "Failed to fetch record" });
    });
});

const {  ObjectId } = require('mongodb');

// ...

// Update a record
app.put('/data/:id', (req, res) => {
    const { id } = req.params;
    const { name, email } = req.body;
    const collection = client.db(dbName).collection(collectionName);
  
    collection
      .updateOne(
        { _id: new ObjectId(id) },
        { $set: { name, email } }
      )
      .then((result) => {
        if (result.matchedCount === 0) {
          return res.status(404).json({ message: 'Record not found' });
        }
        res.json({ message: 'Record updated successfully' });
      })
      .catch((err) => {
        console.error(err);
        res.status(500).json({ message: 'Failed to update record' });
      });
  });
  

// Delete a record
app.delete('/data/:id', (req, res) => {
  const { id } = req.params;
  const collection = client.db(dbName).collection(collectionName);

  collection
    .deleteOne({ _id:new ObjectId(id)})
    .then((result) => {
      if (result.deletedCount === 0) {
        return res.status(404).json({ message: 'Record not found' });
      }
      res.json({ message: 'Record deleted successfully' });
    })
    .catch((err) => {
      console.error(err);
      res.status(500).json({ message: 'Failed to delete record' });
    });
});

// ...


// Start the server
app.listen(8000, () => {
  console.log("Server started on port 8000");
});
