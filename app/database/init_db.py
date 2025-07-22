from app.database.session import Base, engine  
from app.models import customer, subscriptions  

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init()