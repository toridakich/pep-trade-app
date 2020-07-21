from sqlalchemy import Column
from sqlalchemy.dialects.mysql import MEDIUMINT, INTEGER, TINYINT, SMALLINT, VARCHAR, DATETIME, BOOLEAN, DATE, FLOAT
from models.sqla_utils import BASE

class TeamPayroll(BASE):
    year = Column(INTEGER(8))
    team = Column(VARCHAR(3))
    payroll_this_year = Column(INTEGER(8))
    payroll_next_year = Column(INTEGER(8))
    payroll_in_two_years = Column(INTEGER(8))
    payroll_in_three_years = Column(INTEGER(8))
    payroll_in_four_years = Column(INTEGER(8))