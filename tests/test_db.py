import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

# Lấy thông tin từ .env
AWS_PG_HOST = os.getenv("AWS_PG_HOST")
AWS_PG_PORT = os.getenv("AWS_PG_PORT", "5432")
AWS_PG_USER = os.getenv("AWS_PG_USER", "postgres")
AWS_PG_PASSWORD = os.getenv("AWS_PG_PASSWORD")
AWS_PG_DATABASE = os.getenv("AWS_PG_DATABASE", "main_service")

# Tạo URL kết nối cho SQLAlchemy
DATABASE_URL = f"postgresql://{AWS_PG_USER}:{AWS_PG_PASSWORD}@{AWS_PG_HOST}:{AWS_PG_PORT}/{AWS_PG_DATABASE}"

# Tạo engine và session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Kết nối đến DB và thực thi câu lệnh SQL
try:
    with engine.connect() as conn:
        # Sử dụng text() để thực thi câu lệnh SQL
        result = conn.execute(text("SELECT 1;"))
        print("Result:", result.fetchone())  # In ra kết quả của câu lệnh SELECT
except Exception as e:
    print("Error:", e)
