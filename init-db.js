// Connect to the database (this will create the DB if it doesn't exist)
db = db.getSiblingDB('courses_db');

db.createUser({
  user: 'dbuser',
  pwd: 'dbpassword',
  roles: [{ role: 'readWrite', db: 'courses_db' }]
});

// Create collections
db.createCollection('users');
db.createCollection('courses');