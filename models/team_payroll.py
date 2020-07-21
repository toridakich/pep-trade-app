from sqlalchemy import Column
from sqlalchemy.dialects.mysql import MEDIUMINT, INTEGER, TINYINT, SMALLINT, VARCHAR, DATETIME, BOOLEAN, DATE, FLOAT
from models.sqla_utils import BASE

class TeamPayroll(BASE):
    __tablename__ = 'TeamPayroll'

    year = Column(INTEGER(8), primary_key=True)
    team = Column(VARCHAR(3), primary_key=True)
    payroll_this_year = Column(INTEGER(8))
    payroll_next_year = Column(INTEGER(8))
    payroll_in_two_years = Column(INTEGER(8))
    payroll_in_three_years = Column(INTEGER(8))
    payroll_in_four_years = Column(INTEGER(8))
