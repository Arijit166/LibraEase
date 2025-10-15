import pandas as pd
import numpy as np
import os
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        # Create data directory if not exists
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Define file paths
        self.users_file = self.data_dir / "users.csv"
        self.books_file = self.data_dir / "books.csv"
        self.images_dir = Path("data/book_images")
        self.images_dir.mkdir(exist_ok=True)
        
        # Initialize dataframes
        self.init_database()
    
    def init_database(self):
        """Initialize CSV files if they don't exist"""
        # Users CSV
        if not self.users_file.exists():
            users_df = pd.DataFrame(columns=[
                'email', 'first_name', 'last_name', 'password', 'role'
            ])
            users_df.to_csv(self.users_file, index=False)
        
        # Books CSV
        if not self.books_file.exists():
            books_df = pd.DataFrame(columns=[
                'id', 'name', 'author', 'image_path'
            ])
            books_df.to_csv(self.books_file, index=False)
    
    # ==================== USER OPERATIONS ====================
    
    def get_all_users(self):
        """Get all users as DataFrame"""
        return pd.read_csv(self.users_file)
    
    def get_user_by_email(self, email):
        """Get user by email, returns Series or None"""
        df = pd.read_csv(self.users_file)
        user = df[df['email'] == email.lower()]
        if len(user) > 0:
            return user.iloc[0]
        return None
    
    def user_exists(self, email):
        """Check if user exists"""
        df = pd.read_csv(self.users_file)
        return email.lower() in df['email'].values
    
    def create_user(self, email, first_name, last_name, password, role):
        """Create new user"""
        df = pd.read_csv(self.users_file)
        
        new_user = pd.DataFrame([{
            'email': email.lower(),
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'role': role
        }])
        
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv(self.users_file, index=False)
        return True
    
    def validate_login(self, email, password):
        """Validate user login credentials"""
        user = self.get_user_by_email(email)
        if user is not None and user['password'] == password:
            return {
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'role': user['role']
            }
        return None
    
    # ==================== BOOK OPERATIONS ====================
    
    def get_all_books(self):
        """Get all books as DataFrame"""
        df = pd.read_csv(self.books_file)
        # Handle empty dataframe
        if len(df) == 0:
            return df
        # Convert id to int
        df['id'] = df['id'].astype(int)
        return df
    
    def get_book_by_id(self, book_id):
        """Get book by ID"""
        df = pd.read_csv(self.books_file)
        book = df[df['id'] == book_id]
        if len(book) > 0:
            return book.iloc[0]
        return None
    
    def search_books(self, query):
        """Search books by name or author"""
        df = self.get_all_books()
        if len(df) == 0:
            return df
        
        query = query.lower()
        mask = (df['name'].str.lower().str.contains(query, na=False) | 
                df['author'].str.lower().str.contains(query, na=False))
        return df[mask]
    
    def create_book(self, name, author, image_path=None):
        """Create new book"""
        df = pd.read_csv(self.books_file)
        
        # Generate new ID using numpy
        if len(df) > 0:
            new_id = int(np.max(df['id'].values) + 1)
        else:
            new_id = 1
        
        new_book = pd.DataFrame([{
            'id': new_id,
            'name': name,
            'author': author,
            'image_path': image_path if image_path else ''
        }])
        
        df = pd.concat([df, new_book], ignore_index=True)
        df.to_csv(self.books_file, index=False)
        return new_id
    
    def create_book_with_id(self, book_id, name, author, image_path=None):
        """Create new book with specific ID"""
        df = pd.read_csv(self.books_file)
        
        # Check if ID already exists
        if book_id in df['id'].values:
            raise ValueError(f"Book ID {book_id} already exists")
        
        new_book = pd.DataFrame([{
            'id': book_id,
            'name': name,
            'author': author,
            'image_path': image_path if image_path else ''
        }])
        
        df = pd.concat([df, new_book], ignore_index=True)
        df.to_csv(self.books_file, index=False)
        return book_id
    
    def update_book(self, book_id, name=None, author=None, image_path=None):
        """Update book information"""
        df = pd.read_csv(self.books_file)
        
        # Find book index
        idx = df[df['id'] == book_id].index
        if len(idx) == 0:
            return False
        
        idx = idx[0]
        
        # Update fields
        if name is not None:
            df.at[idx, 'name'] = name
        if author is not None:
            df.at[idx, 'author'] = author
        if image_path is not None:
            df.at[idx, 'image_path'] = image_path
        
        df.to_csv(self.books_file, index=False)
        return True
    
    def delete_book(self, book_id):
        """Delete book by ID"""
        df = pd.read_csv(self.books_file)
        
        # Get image path before deleting
        book = df[df['id'] == book_id]
        if len(book) > 0:
            image_path = book.iloc[0]['image_path']
            
            # Delete from dataframe
            df = df[df['id'] != book_id]
            df.to_csv(self.books_file, index=False)
            
            # Return image path for deletion
            return image_path if pd.notna(image_path) and image_path else None
        
        return None
    
    def get_book_count(self):
        """Get total number of books using numpy"""
        df = self.get_all_books()
        return np.int64(len(df))
    
    def get_books_by_author(self, author):
        """Get all books by a specific author"""
        df = self.get_all_books()
        return df[df['author'].str.lower() == author.lower()]
    
    # ==================== ANALYTICS (using numpy) ====================
    
    def get_user_stats(self):
        """Get user statistics using numpy"""
        df = pd.read_csv(self.users_file)
        
        if len(df) == 0:
            return {'total': 0, 'admins': 0, 'users': 0}
        
        role_counts = df['role'].value_counts()
        
        return {
            'total': int(np.int64(len(df))),
            'admins': int(role_counts.get('Admin', 0)),
            'users': int(role_counts.get('User', 0))
        }
    
    def get_book_stats(self):
        """Get book statistics using numpy"""
        df = self.get_all_books()
        
        if len(df) == 0:
            return {'total': 0, 'with_images': 0}
        
        # Count books with images using numpy
        has_image = df['image_path'].notna() & (df['image_path'] != '')
        
        return {
            'total': int(np.int64(len(df))),
            'with_images': int(np.sum(has_image))
        }