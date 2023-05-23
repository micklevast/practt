const express = require('express');
const cors = require('cors');
const mysql = require('mysql');

// Create a new Express app
const app = express();

// Enable Cross-Origin Resource Sharing
app.use(cors());
app.use(express.json());

// Create MySQL connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'Vishal@20',
  database: 'vishal',
});

// Connect to the database
db.connect((err) => {
  if (err) {
    throw err;
  }
  console.log('Connected to MySQL database');
});

// Create a new record
app.post("/data", (req,res)=>{
    var name=req.body.name;
    var id=req.body.id;
    var email=req.body.email;
    const sql = `INSERT INTO ads (name, id, email) VALUES (?,?, ?)`;
    db.query(sql, [name,id,email], (err,result)=>{
        if(err) throw err;
        else res.json({ message: 'Record created successfully', id: result.insertId });
    })
})

// Read all records
app.get('/data', (req, res) => {
  const sql = 'SELECT * FROM ads';

  db.query(sql, (err, result) => {
    if (err) {
      throw err;
    }
    res.json(result);
  });
});

// Read a single record
app.get('/data/:id', (req, res) => {
  const { id } = req.params;
  const sql = `SELECT * FROM ads WHERE id = ${id}`;

  db.query(sql, [id], (err, result) => {
    if (err) {
      throw err;
    }
    if (result.length === 0) {
      return res.status(404).json({ message: 'Record not found' });
    }
    res.json(result[0]);
  });
});

// Update a record
app.put('/data/:id', (req, res) => {
    const { id } = req.params;
    const { name, email } = req.body;
    const sql = `UPDATE ads SET name = ?, email = ? WHERE id = ?`;
  
    db.query(sql, [name, email, id], (err, result) => {
      if (err) {
        throw err;
      }
      if (result.affectedRows === 0) {
        return res.status(404).json({ message: 'Record not found' });
      }
      res.json({ message: 'Record updated successfully' });
    });
  });

// Delete a record
app.delete('/data/:id', (req, res) => {
  const { id } = req.params;
  const sql = `DELETE FROM ads WHERE id = ${id}`;

  db.query(sql, [id], (err) => {
    if (err) {
      throw err;
    }
    res.json({ message: 'Record deleted successfully' });
  });
});

// Start the server
app.listen(5000, () => {
  console.log('Server started on port 5000');
});






// dsgfdf,mbnkfgmbkmfgkbm kdf,v bl;f,b lcxfmblk,df==============

import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState([]);
  const [formData, setFormData] = useState({ name: "", id: "", email: "" });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get("http://localhost:5000/data");
      setData(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCreate = async () => {
    try {
      await axios.post("http://localhost:5000/data", formData);
      setFormData({ id: "", name: "", email: "" });
      fetchData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleEdit = (id) => {
    const selectedRecord = data.find((item) => item.id === id);
    setEditingId(id);
    setFormData({
      id: selectedRecord.id,
      name: selectedRecord.name,
      email: selectedRecord.email,
    });
  };

  const handleUpdate = async () => {
    try {
      await axios.put(`http://localhost:5000/data/${editingId}`, formData);
      setEditingId(null);
      setFormData({ id: "", name: "", email: "" });
      fetchData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setFormData({ id: "", name: "", email: "" });
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/data/${id}`);
      fetchData();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Data from the MySQL database</h1>
      <ul>
        {data.map((item) => (
          <li key={item.id}>
            {item.name} - {item.id} - {item.email}
            {!editingId && (
              <>
                <button onClick={() => handleEdit(item.id)}>Edit</button>
                <button onClick={() => handleDelete(item.id)}>Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>
      {editingId ? (
        <>
          <h2>Edit Record:</h2>
          <form>
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={formData.name}
              onChange={handleInputChange}
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
            />
            <button type="button" onClick={handleUpdate}>
              Update
            </button>
            <button type="button" onClick={handleCancelEdit}>
              Cancel
            </button>
          </form>
        </>
      ) : (
        <>
          <h2>Add a new record:</h2>
          <form>
            <input
              type="number"
              name="id"
              placeholder="id"
              value={formData.id}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={formData.name}
              onChange={handleInputChange}
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
            />
            <button type="button" onClick={handleCreate}>
              Create
            </button>
          </form>
        </>
      )}
    </div>
  );
}

export default App;
