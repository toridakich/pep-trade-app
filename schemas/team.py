from marshmallow import Schema, fields, validate, pre_dump, post_dump
import re

class Team(Schema):


    team = fields.String()
    year = fields.Integer()
    league = fields.String()
    W = fields.Integer()
    L = fields.Integer()
    win_pct = fields.Float()
    homeW = fields.Integer()
    homeL = fields.Integer()
    awayW = fields.Integer()
    awayL = fields.Integer()
    RS = fields.Integer()
    RA = fields.Integer()
    DIFF = fields.Integer()
    exp_win_pct = fields.Float()
    PA = fields.Integer()
    AB = fields.Integer()
    S = fields.Integer()
    D = fields.Integer()
    T = fields.Integer()
    HR = fields.Integer()
    TB = fields.Integer()
    H = fields.Integer()
    R = fields.Integer()
    RBI = fields.Integer()
    SB = fields.Integer()
    CS = fields.Integer()
    BB = fields.Integer()
    IBB = fields.Integer()
    SO = fields.Integer()
    HBP = fields.Integer()
    SF = fields.Integer()
    SH = fields.Integer()
    AVG = fields.Float()
    OBP = fields.Float()
    SLG = fields.Float()
    OPS = fields.Float()
    wOBA = fields.Float()
    wRAA = fields.Float()
    BF = fields.Integer()
    IP = fields.Float()
    Ha = fields.Integer()
    HRa = fields.Integer()
    TBa = fields.Integer()
    BBa = fields.Integer()
    IBBa = fields.Integer()
    IFFB = fields.Integer()
    K = fields.Integer()
    HBPa = fields.Integer()
    BK = fields.Integer()
    W = fields.Integer()
    L = fields.Integer()
    SV = fields.Integer()
    TR = fields.Integer()
    ER = fields.Integer()
    RAA = fields.Float()
    ERA = fields.Float()
    FIP = fields.Float()
    SpIP = fields.Float()
    RpIP = fields.Float()
    SpER = fields.Integer()
    RpER = fields.Integer()
    SpTR = fields.Integer()
    RpTR = fields.Integer()
    SpERA = fields.Float()
    SpFIP = fields.Float()
    RpERA = fields.Float()
    RpFIP = fields.Float()
    PPFp = fields.Float()
