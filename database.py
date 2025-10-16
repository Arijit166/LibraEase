import pandas as pd
import numpy as np
import os
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        # Create data directory if not exists
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.borrowed_file = self.data_dir / "borrowed.csv"
        
        # Define file paths
        self.users_file = self.data_dir / "users.csv"
        self.books_file = self.data_dir / "books.csv"
        self.cart_file = self.data_dir / "cart.csv"
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
                'id', 'name', 'author', 'image_path', 'count'
            ])
            books_df.to_csv(self.books_file, index=False)

        # Cart CSV
        if not self.cart_file.exists():
            cart_df = pd.DataFrame(columns=[
                'user_email', 'book_id'
            ])
            cart_df.to_csv(self.cart_file, index=False)

        # Borrowed Books CSV
        if not self.borrowed_file.exists():
            borrowed_df = pd.DataFrame(columns=[
                'user_email', 'book_id', 'issue_date', 'collection_deadline', 
                'return_deadline', 'status', 'collected', 'collection_date', 'return_date'
            ])
            borrowed_df.to_csv(self.borrowed_file, index=False)
    
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
        """Search books by name, author or ID"""
        df = self.get_all_books()
        if len(df) == 0:
            return df
        
        query = str(query).lower()
        
        # Search by name, author, or ID (as string)
        mask = (df['name'].str.lower().str.contains(query, na=False) | 
                df['author'].str.lower().str.contains(query, na=False) |
                df['id'].astype(str).str.contains(query, na=False))
        
        return df[mask]
    
    def create_book(self, name, author, image_path=None, count=1):
        """Create new book"""
        df = pd.read_csv(self.books_file)
        
        if len(df) > 0:
            new_id = int(np.max(df['id'].values) + 1)
        else:
            new_id = 1
        
        new_book = pd.DataFrame([{
            'id': new_id,
            'name': name,
            'author': author,
            'image_path': image_path if image_path else '',
            'count': count  # Added
        }])
        
        df = pd.concat([df, new_book], ignore_index=True)
        df.to_csv(self.books_file, index=False)
        return new_id
    
    def create_book_with_id(self, book_id, name, author, image_path=None, count=1):
        """Create new book with specific ID"""
        df = pd.read_csv(self.books_file)
        
        if book_id in df['id'].values:
            raise ValueError(f"Book ID {book_id} already exists")
        
        new_book = pd.DataFrame([{
            'id': book_id,
            'name': name,
            'author': author,
            'image_path': image_path if image_path else '',
            'count': count  
        }])
        
        df = pd.concat([df, new_book], ignore_index=True)
        df.to_csv(self.books_file, index=False)
        return book_id
    
    def update_book(self, book_id, name=None, author=None, image_path=None, count=None):
        """Update book information"""
        df = pd.read_csv(self.books_file)
        
        idx = df[df['id'] == book_id].index
        if len(idx) == 0:
            return False
        
        idx = idx[0]
        
        if name is not None:
            df.at[idx, 'name'] = name
        if author is not None:
            df.at[idx, 'author'] = author
        if image_path is not None:
            df.at[idx, 'image_path'] = image_path
        if count is not None:  # Added
            df.at[idx, 'count'] = count
        
        df.to_csv(self.books_file, index=False)
        return True

    # Add method to decrease count when borrowing:
    def decrease_book_count(self, book_id):
        """Decrease book count by 1"""
        df = pd.read_csv(self.books_file)
        idx = df[df['id'] == book_id].index
        if len(idx) == 0:
            return False
        
        idx = idx[0]
        current_count = df.at[idx, 'count']
        if current_count > 0:
            df.at[idx, 'count'] = current_count - 1
            df.to_csv(self.books_file, index=False)
            return True
        return False

    # Add method to increase count when returning:
    def increase_book_count(self, book_id):
        """Increase book count by 1"""
        df = pd.read_csv(self.books_file)
        idx = df[df['id'] == book_id].index
        if len(idx) == 0:
            return False
        
        idx = idx[0]
        df.at[idx, 'count'] = df.at[idx, 'count'] + 1
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
    
    # ==================== CART OPERATIONS ====================
    
    def add_to_cart(self, user_email, book_id):
        """Add book to user's cart"""
        df = pd.read_csv(self.cart_file)
        
        # Check if already in cart
        if self.is_in_cart(user_email, book_id):
            return False  # Already exists
        
        new_item = pd.DataFrame([{
            'user_email': user_email.lower(),
            'book_id': book_id
        }])
        
        df = pd.concat([df, new_item], ignore_index=True)
        df.to_csv(self.cart_file, index=False)
        return True

    def remove_from_cart(self, user_email, book_id):
        """Remove book from user's cart"""
        df = pd.read_csv(self.cart_file)
        
        # Remove the item
        df = df[~((df['user_email'] == user_email.lower()) & (df['book_id'] == book_id))]
        df.to_csv(self.cart_file, index=False)
        return True

    def is_in_cart(self, user_email, book_id):
        """Check if book is in user's cart"""
        df = pd.read_csv(self.cart_file)
        mask = (df['user_email'] == user_email.lower()) & (df['book_id'] == book_id)
        return np.any(mask)

    def get_user_cart(self, user_email):
        """Get all cart items for a user with book details"""
        cart_df = pd.read_csv(self.cart_file)
        books_df = self.get_all_books()
        
        # Filter cart for this user
        user_cart = cart_df[cart_df['user_email'] == user_email.lower()]
        
        if len(user_cart) == 0:
            # Return empty DataFrame with correct columns matching books structure
            return pd.DataFrame(columns=['id', 'name', 'author', 'image_path'])
        
        # Get book IDs from cart
        book_ids = user_cart['book_id'].values
        
        # Filter books that are in cart
        cart_books = books_df[books_df['id'].isin(book_ids)]
        
        # Handle case where books were deleted but still in cart
        if len(cart_books) == 0:
            return pd.DataFrame(columns=['id', 'name', 'author', 'image_path'])
        
        return cart_books
    
    def get_cart_count(self, user_email):
        """Get number of items in user's cart using numpy"""
        df = pd.read_csv(self.cart_file)
        user_cart = df[df['user_email'] == user_email.lower()]
        return int(np.int64(len(user_cart)))

    def clear_cart(self, user_email):
        """Clear all items from user's cart"""
        df = pd.read_csv(self.cart_file)
        df = df[df['user_email'] != user_email.lower()]
        df.to_csv(self.cart_file, index=False)
        return True
    
    # ==================== BORROWING OPERATIONS ====================
    
    def can_borrow_book(self, user_email):
        """Check if user can borrow more books (max 2)"""
        df = pd.read_csv(self.borrowed_file)
        user_borrowed = df[(df['user_email'] == user_email.lower()) & 
                        (df['status'] == 'borrowed')]
        return len(user_borrowed) < 2
    
    def is_book_borrowed_by_user(self, user_email, book_id):
        """Check if a specific user has borrowed a specific book and it's still active"""
        df = pd.read_csv(self.borrowed_file)
        borrowed = df[(df['user_email'] == user_email.lower()) & 
                    (df['book_id'] == book_id) & 
                    (df['status'] == 'borrowed')]
        return len(borrowed) > 0

    def user_has_borrowed_book(self, user_email, book_id):
        """Check if user has already borrowed this specific book"""
        df = pd.read_csv(self.borrowed_file)
        borrowed = df[(df['user_email'] == user_email.lower()) & 
                    (df['book_id'] == book_id) & 
                    (df['status'] == 'borrowed')]
        return len(borrowed) > 0

    def borrow_book(self, user_email, book_id):
        """Borrow a book"""
        from datetime import datetime, timedelta
        
        if not self.can_borrow_book(user_email):
            return {'success': False, 'message': 'You can only borrow maximum 2 books at a time!'}
        
        if self.user_has_borrowed_book(user_email, book_id):
            return {'success': False, 'message': 'You have already borrowed this book!'}
        
        # Check if book is available
        book = self.get_book_by_id(book_id)
        if book is None or book.get('count', 0) <= 0:
            return {'success': False, 'message': 'This book is currently not available!'}
        
        # Decrease book count
        if not self.decrease_book_count(book_id):
            return {'success': False, 'message': 'Failed to borrow book!'}
        
        df = pd.read_csv(self.borrowed_file)
        
        if 'collected' not in df.columns:
            df['collected'] = False
        if 'collection_date' not in df.columns:
            df['collection_date'] = ''
        if 'return_date' not in df.columns:
            df['return_date'] = ''
        
        issue_date = datetime.now()
        collection_deadline = issue_date + timedelta(days=3)
        return_deadline = issue_date + timedelta(days=45)
        
        new_borrow = pd.DataFrame([{
            'user_email': user_email.lower(),
            'book_id': book_id,
            'issue_date': issue_date.isoformat(),
            'collection_deadline': collection_deadline.isoformat(),
            'return_deadline': return_deadline.isoformat(),
            'status': 'borrowed',
            'collected': False,
            'collection_date': '',
            'return_date': ''
        }])
        
        df = pd.concat([df, new_borrow], ignore_index=True)
        df.to_csv(self.borrowed_file, index=False)
        
        self.remove_from_cart(user_email, book_id)
        
        return {
            'success': True, 
            'collection_deadline': collection_deadline.strftime('%d %B %Y'),
            'return_deadline': return_deadline.strftime('%d %B %Y')
        }

    def get_user_borrowed_books(self, user_email):
        """Get all borrowed books for a user with book details"""
        borrowed_df = pd.read_csv(self.borrowed_file)
        books_df = self.get_all_books()
        
        # Add missing columns if they don't exist
        if 'collected' not in borrowed_df.columns:
            borrowed_df['collected'] = False
        if 'collection_date' not in borrowed_df.columns:
            borrowed_df['collection_date'] = ''
        if 'return_date' not in borrowed_df.columns:
            borrowed_df['return_date'] = ''
        
        # Filter borrowed books for this user
        user_borrowed = borrowed_df[borrowed_df['user_email'] == user_email.lower()]
        
        if len(user_borrowed) == 0:
            return pd.DataFrame(columns=['id', 'name', 'author', 'image_path', 
                                        'issue_date', 'collection_deadline', 
                                        'return_deadline', 'status', 'collected',
                                        'collection_date', 'return_date'])
        
        # Merge with books data
        merged = user_borrowed.merge(books_df, left_on='book_id', right_on='id', how='left')
        
        # Select and rename columns - include all new columns
        result = merged[['id', 'name', 'author', 'image_path', 'issue_date', 
                        'collection_deadline', 'return_deadline', 'status', 
                        'collected', 'collection_date', 'return_date']]
        
        # Sort by issue date (most recent first)
        result = result.sort_values('issue_date', ascending=False)
        
        return result

    def get_borrowed_count(self, user_email):
        """Get count of currently borrowed books"""
        df = pd.read_csv(self.borrowed_file)
        borrowed = df[(df['user_email'] == user_email.lower()) & 
                    (df['status'] == 'borrowed')]
        return int(np.int64(len(borrowed)))

    def return_book(self, user_email, book_id):
        """Mark a book as returned (for admin use)"""
        df = pd.read_csv(self.borrowed_file)
        
        # Find the borrowed record
        mask = ((df['user_email'] == user_email.lower()) & 
                (df['book_id'] == book_id) & 
                (df['status'] == 'borrowed'))
        
        if not np.any(mask):
            return False
        
        # Update status to returned
        df.loc[mask, 'status'] = 'returned'
        df.to_csv(self.borrowed_file, index=False)
        return True
    
    # ==================== ADMIN BORROWING OPERATIONS ====================

    def get_all_borrowed_books(self):
        """Get all borrowed books with user and book details for admin"""
        borrowed_df = pd.read_csv(self.borrowed_file)
        books_df = self.get_all_books()
        users_df = self.get_all_users()
        
        if len(borrowed_df) == 0:
            return pd.DataFrame(columns=['user_email', 'user_name', 'book_id', 'name', 
                                        'author', 'image_path', 'issue_date', 
                                        'collection_deadline', 'return_deadline', 
                                        'status', 'collected'])
        
        # Add collected column if not exists
        if 'collected' not in borrowed_df.columns:
            borrowed_df['collected'] = False
        
        # Merge with books data
        merged = borrowed_df.merge(books_df, left_on='book_id', right_on='id', how='left')
        
        # Merge with users data to get names
        merged = merged.merge(
            users_df[['email', 'first_name', 'last_name']], 
            left_on='user_email', 
            right_on='email', 
            how='left'
        )
        
        # Create full name
        merged['user_name'] = merged['first_name'] + ' ' + merged['last_name']
        
        # Select required columns
        result = merged[['user_email', 'user_name', 'book_id', 'name', 'author', 
                        'image_path', 'issue_date', 'collection_deadline', 
                        'return_deadline', 'status', 'collected']]
        
        # Sort by issue date (most recent first)
        result = result.sort_values('issue_date', ascending=False)
        
        return result

    def mark_book_collected(self, user_email, book_id):
        """Mark a borrowed book as collected by user"""
        from datetime import datetime
        
        df = pd.read_csv(self.borrowed_file)
        
        # Add collected column if not exists
        if 'collected' not in df.columns:
            df['collected'] = False
        
        # Add collection_date column if not exists
        if 'collection_date' not in df.columns:
            df['collection_date'] = ''
        
        # Find the borrowed record
        mask = ((df['user_email'] == user_email.lower()) & 
                (df['book_id'] == book_id) & 
                (df['status'] == 'borrowed'))
        
        if not np.any(mask):
            return False
        
        # Update collected status and date
        df.loc[mask, 'collected'] = True
        df.loc[mask, 'collection_date'] = datetime.now().isoformat()
        df.to_csv(self.borrowed_file, index=False)
        return True

    def mark_book_returned(self, user_email, book_id):
        """Mark a borrowed book as returned"""
        from datetime import datetime
        
        df = pd.read_csv(self.borrowed_file)
        
        if 'return_date' not in df.columns:
            df['return_date'] = ''
        
        mask = ((df['user_email'] == user_email.lower()) & 
                (df['book_id'] == book_id) & 
                (df['status'] == 'borrowed'))
        
        if not np.any(mask):
            return False
        
        df.loc[mask, 'status'] = 'returned'
        df.loc[mask, 'return_date'] = datetime.now().isoformat()
        df.to_csv(self.borrowed_file, index=False)
        
        # Increase book count
        self.increase_book_count(book_id)
        
        return True

    def get_borrowed_stats(self):
        """Get borrowing statistics for admin"""
        df = pd.read_csv(self.borrowed_file)
        
        if len(df) == 0:
            return {
                'total_borrowed': 0,
                'active_borrowed': 0,
                'pending_collection': 0,
                'collected': 0,
                'returned': 0
            }
        
        # Add collected column if not exists
        if 'collected' not in df.columns:
            df['collected'] = False
        
        active = df[df['status'] == 'borrowed']
        
        return {
            'total_borrowed': int(np.int64(len(df))),
            'active_borrowed': int(np.int64(len(active))),
            'pending_collection': int(np.sum((active['collected'] == False).values)),
            'collected': int(np.sum((active['collected'] == True).values)),
            'returned': int(np.int64(len(df[df['status'] == 'returned'])))
        }