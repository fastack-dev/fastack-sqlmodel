from typing import List

from app.models import Book
from fastack import CRUDController
from fastapi import Request, status
from fastapi.responses import Response
from pydantic import BaseModel, conint, constr
from sqlalchemy.sql.expression import desc
from sqlmodel import select

from fastack_sqlmodel.session import Session


class BodyBookModel(BaseModel):
    title: constr(max_length=255)
    status: Book.Status = Book.Status.DRAFT


class BookController(CRUDController):
    def retrieve(self, request: Request, id: int) -> Response:
        session: Session = request.state.db.open()
        with session:
            qs = select(Book).where(Book.id == id)
            book: Book = session.exec(qs).first()
            if not book:
                return self.json("Not found", status=status.HTTP_404_NOT_FOUND)

            return self.json("Detail book", book)

    def list(
        self, request: Request, page: conint(gt=0) = 1, page_size: conint(gt=0) = 10
    ) -> Response:
        session: Session = request.state.db.open()
        with session:
            books: List[Book] = session.exec(
                select(Book).order_by(desc(Book.date_created))
            ).all()
            return self.get_paginated_response(books, page, page_size)

    def create(self, request: Request, body: BodyBookModel) -> Response:
        session: Session = request.state.db.open()
        with session.begin():
            data = body.dict()
            book: Book = Book.create(session, **data)

        return self.json("Created", book)

    def update(self, request: Request, id: int, body: BodyBookModel) -> Response:
        session: Session = request.state.db.open()
        with session.begin():
            book = session.exec(select(Book).where(Book.id == id)).first()
            if not book:
                return self.json("Not found", status=status.HTTP_404_NOT_FOUND)

            data = body.dict()
            book.update(session, **data)

        return self.json("Updated", book)

    def destroy(self, request: Request, id: int) -> Response:
        session: Session = request.state.db.open()
        with session.begin():
            book: Book = session.exec(select(Book).where(Book.id == id)).first()
            if not book:
                return self.json("Not found", status=status.HTTP_404_NOT_FOUND)

            book.delete(session)

        return self.json("Deleted")
