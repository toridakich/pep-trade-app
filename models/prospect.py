from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import MEDIUMINT, INTEGER, TINYINT, SMALLINT, VARCHAR, DATETIME, BOOLEAN, DATE, FLOAT
from sqlalchemy.orm import relationship
from models.team import Team
from models.sqla_utils import PROSPECTBASE

class Prospect(PROSPECTBASE):
    __tablename__ = 'Prospect'

    name = Column(VARCHAR(50), primary_key=True)
    ml_team = Column(VARCHAR(3), primary_key=True)
    year = Column(INTEGER(4), primary_key=True)
    team = Column(VARCHAR(50))
    ETA = Column(INTEGER(4))
    position = Column(VARCHAR(15))
    draft_year = Column(INTEGER(4))
    draft_pos = Column(INTEGER(4))
    draft_round = Column(INTEGER(4))
    mlb_rank = Column(INTEGER(4))
    team_rank = Column(INTEGER(4))
    Fastball = Column(INTEGER(4))
    Slider = Column(INTEGER(4))
    Curveball = Column(INTEGER(4))
    Changeup = Column(INTEGER(4))
    Cutter = Column(INTEGER(4))
    Control = Column(INTEGER(4))
    Hit = Column(INTEGER(4))
    Power = Column(INTEGER(4))
    Run = Column(INTEGER(4))
    Arm = Column(INTEGER(4))
    Field = Column(INTEGER(4))
    Overall = Column(INTEGER(4))

