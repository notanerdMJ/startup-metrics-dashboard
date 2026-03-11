# backend/test_register.py
"""Test registration step by step."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Step 1: Test database connection
print("=== Step 1: Database Connection ===")
try:
    from app.database import engine, SessionLocal, Base
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("  ✅ Database connected")
except Exception as e:
    print(f"  ❌ Database error: {e}")
    sys.exit(1)

# Step 2: Create tables
print("\n=== Step 2: Create Tables ===")
try:
    from app.models.user import User
    from app.models.raw_data import RawData
    from app.models.metrics import CalculatedMetrics
    from app.models.insight import AIInsight
    from app.models.chat import ChatHistory
    
    Base.metadata.create_all(bind=engine)
    
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"  Tables: {tables}")
    
    if "users" in tables:
        print("  ✅ Users table exists")
    else:
        print("  ❌ Users table missing!")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Table creation error: {e}")
    sys.exit(1)

# Step 3: Test password hashing
print("\n=== Step 3: Password Hashing ===")
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_context.hash("test123456")
    print(f"  Hashed: {hashed[:30]}...")
    verified = pwd_context.verify("test123456", hashed)
    print(f"  Verified: {verified}")
    print("  ✅ Bcrypt working")
except Exception as e:
    print(f"  ❌ Bcrypt error: {e}")
    print("  Trying to install bcrypt...")
    os.system("pip install bcrypt passlib[bcrypt]")
    sys.exit(1)

# Step 4: Test JWT
print("\n=== Step 4: JWT Token ===")
try:
    import jwt
    from app.config import settings
    token = jwt.encode({"sub": "1", "email": "test@test.com"}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    print(f"  Token: {token[:30]}...")
    decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    print(f"  Decoded: {decoded}")
    print("  ✅ JWT working")
except Exception as e:
    print(f"  ❌ JWT error: {e}")
    sys.exit(1)

# Step 5: Test actual registration
print("\n=== Step 5: Test Registration ===")
try:
    db = SessionLocal()
    
    # Check if user already exists
    existing = db.query(User).filter(User.email == "test_debug@test.com").first()
    if existing:
        db.delete(existing)
        db.commit()
        print("  Deleted existing test user")
    
    # Create user
    from app.services.auth_service import create_user, verify_password
    user = create_user(db, "test_debug@test.com", "Debug User", "test123456")
    print(f"  Created user: id={user.id}, email={user.email}")
    
    # Verify password
    is_valid = verify_password("test123456", user.hashed_password)
    print(f"  Password verify: {is_valid}")
    
    # Create token
    from app.services.auth_service import create_access_token
    token = create_access_token(user.id, user.email)
    print(f"  Token: {token[:30]}...")
    
    # Clean up
    db.delete(user)
    db.commit()
    db.close()
    
    print("  ✅ Registration works!")
    
except Exception as e:
    print(f"  ❌ Registration error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== DIAGNOSTIC COMPLETE ===")