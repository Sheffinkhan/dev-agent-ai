import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("GitDetails.db")
cursor = conn.cursor()

# Database schema for Git details
schema = """
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,  -- Added UNIQUE constraint to prevent duplicate branches
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Commits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id INTEGER,
    user_id INTEGER,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES Branches(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
"""

# Execute schema setup
cursor.executescript(schema)

# Insert sample users
users = [
    ("Alice Johnson", "alice@example.com"),
    ("Bob Smith", "bob@example.com"),
    ("Charlie Brown", "charlie@example.com")
]
cursor.executemany("INSERT OR IGNORE INTO Users (name, email) VALUES (?, ?);", users)

# Insert sample branches
branches = [
    ("main", 1),
    ("feature-login", 2),
    ("bugfix-404", 3)
]
cursor.executemany("INSERT OR IGNORE INTO Branches (name, user_id) VALUES (?, ?);", branches)

# Insert sample commits
commits = [
    (1, 1, "Initial commit"),
    (1, 1, "Added README file"),
    (2, 2, "Implemented user login feature"),
    (2, 2, "Fixed authentication bug"),
    (3, 3, "Resolved 404 page issue"),
    (3, 3, "Updated error message for missing pages")
]
cursor.executemany("INSERT INTO Commits (branch_id, user_id, message) VALUES (?, ?, ?);", commits)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database initialized successfully with sample data.")
