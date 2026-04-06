from app import app, db, User, Task
import os

def test_initialization():
    print("Testing database initialization...")
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database created and models verified.")
            
            # Check for initial user count
            user_count = User.query.count()
            print(f"✅ Current user count: {user_count}")
            
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False
    return True

if __name__ == "__main__":
    if test_initialization():
        print("\nAll backend systems are ready for user registration!")
    else:
        print("\nBackend diagnostic failed. Check logs above.")
