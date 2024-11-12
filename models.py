from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy ORM
db = SQLAlchemy()

class File(db.Model):
    """Model for storing file details in the database."""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    ipfs_hash = db.Column(db.String(120), unique=True, nullable=False)
    pinned = db.Column(db.Boolean, default=True)  # Whether the file is pinned in IPFS

    def __repr__(self):
        return f"<File {self.filename} - {self.ipfs_hash}>"
