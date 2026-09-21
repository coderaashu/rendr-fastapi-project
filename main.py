from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models,schemas
from auth import create_token,verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#login api
@app.post("/login")
def login():
    return{
        "access_token": create_token({"user":"admin"}),
        "token_type":"bearer"
    }

@app.get("/")
def home():
    return {
        "msg":"blog api started"
    }

#create blog (protected)
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate, db:Session = Depends(get_db),user = Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

#read all blog
@app.get("/blogs", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()

#read one blog
@app.get("/blogs/{id}", response_model=schemas.BlogResponse)
def get_blog(id: int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404,detail="Blog not found")
    return blog

#update blog api
@app.put("/blogs/{id}", response_model=schemas.BlogResponse)
def update_blog(id: int,blog:schemas.BlogCreate,db: Session = Depends(get_db),user = Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not existing_blog:
        raise HTTPException(status_code=404,detail="Blog not found")
    existing_blog.title = blog.title
    existing_blog.content = blog.content

    db.commit()
    db.refresh(existing_blog)
    return existing_blog

#delete blog api
@app.delete("/blogs/{id}")
def delete_blog(id: int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404,detail="Blog not found")
    blog.delete()
    db.commit()

    return{
        "Msg":"Blog deleted successfully"
    }

