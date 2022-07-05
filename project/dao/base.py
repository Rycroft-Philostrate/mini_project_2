from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from sqlalchemy import desc
from werkzeug.exceptions import NotFound
from project.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, status: Optional[str] = None, page: Optional[int] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if status == 'new':
            stmt = stmt.order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def get_by_email(self, email: str) -> Optional[T]:
        return self._db_session.query(self.__model__).filter(self.__model__.email == email).one_or_none()

    def create(self, data) -> Optional[T]:
        ent = self.__model__(**data)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def update_partial(self, data):
        self._db_session.add(data)
        self._db_session.commit()

    def get_favorite(self, movie_id, user_id) -> Optional[T]:
        return self._db_session.query(self.__model__).filter(self.__model__.movie_id == movie_id and self.__model__.user_id == user_id).one_or_none()

    def delete(self, data):
        self._db_session.delete(data)
        self._db_session.commit()

