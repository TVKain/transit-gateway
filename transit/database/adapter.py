from contextlib import contextmanager

from sqlmodel import create_engine

from oslo_config import cfg

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class DBAdapter:
    _engine = None
    _session = None

    def __init__(self):

        if self._engine is None:
            self._engine = create_engine(cfg.CONF.database.connection)
            self._session = sessionmaker(bind=self._engine)

    @contextmanager
    def get_session(self):
        session = self._session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
