from sqlalchemy import Column
from sqlalchemy.dialects.mysql import MEDIUMINT, INTEGER, TINYINT, SMALLINT, VARCHAR, DATETIME, BOOLEAN, DATE, FLOAT
from models.sqla_utils import BASE

class PlayerContract(BASE):
    __tablename__ = 'PlayerContract'

    year = Column(INTEGER(4), primary_key=True, default = 0, autoincrement=True)
    team = Column(VARCHAR(3), primary_key=True, default = '')
    player = Column(VARCHAR(50), primary_key=True, default = '')
    length = Column(INTEGER(2))
    value = Column(INTEGER(10))
    free_agent_year = Column(INTEGER(4))