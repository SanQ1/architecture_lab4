class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost:5432/db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
