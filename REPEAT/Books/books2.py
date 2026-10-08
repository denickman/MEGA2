from typing import Optional

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
from starlette import status

class BookCategory(Enum):
    SCIENCE = "science"
    HISTORY = "history"
    MATH = "math"

class RatingLimits:
    MIN = 0
    MAX = 5

class DateLimits:
    MIN = 1999
    MAX = 2031

class Book:
    id: int
    title: str
    description: str
    author: str
    rating: int
    publish_date: str

    def __init__(self, id, title, description, author, rating, publish_date):
        self.id = id
        self.title = title
        self.description = description
        self.author = author
        self.rating = rating
        self.publish_date = publish_date



class BookRequest(BaseModel):
    id: int | None = Field(description="ID is not needed on create", default=None)
    title: str = Field(..., min_length=3)
    author: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1, max_length=100)
    rating: int = Field(ge=RatingLimits.MIN, le=RatingLimits.MAX)
    publish_date: int = Field(gt=DateLimits.MIN, lt=DateLimits.MAX)



    # for showing in swagger
    class Config:
        schema_extra = {
                "example": {
                    "title": "A new book",
                    "author": "codingwithroby",
                    "description": "A new description of a book",
                    "rating": 5,
                    "publish_date": 2029,
                }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2028),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


app = FastAPI()


# ======= GET =========

@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")



@app.get('/books/', status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(ge=RatingLimits.MIN, le=RatingLimits.MAX)):
    books_to_retrieve = []

    for book in BOOKS:
        if book.rating == book_rating:
            books_to_retrieve.append(book)
    return books_to_retrieve



@app.get('/books/publish/')
async def read_book_by_published_date(published_date: int = Query(gt=DateLimits.MIN, le=DateLimits.MAX)):
    books_to_return = []

    for book in BOOKS:
        if book.publish_date == published_date:
            books_to_return.append(book)
    return books_to_return





# ======= POST =========

@app.post('/create_book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))




# ======= PUT =========
@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):

    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i].title = book.title
            BOOKS[i].description = book.description
            BOOKS[i].author = book.author
            BOOKS[i].rating = book.rating
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


# ======= Delete =========
@app.delete('/books/{book_id}')
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False

    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")






# ====== Methods =======

def find_book_id(book: Book):

  #  book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book



