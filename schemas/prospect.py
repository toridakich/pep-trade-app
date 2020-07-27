from marshmallow import Schema, fields, pre_dump

class Prospect(Schema):
    name = fields.String()
    ml_team = fields.String()
    year = fields.Integer()
    team = fields.String()
    ETA = fields.Integer()
    position = fields.String()
    draft_year = fields.Integer()
    draft_pos = fields.Integer()
    draft_round = fields.Integer()
    mlb_rank = fields.Integer()
    team_rank = fields.Integer()
    Fastball = fields.Integer()
    Slider = fields.Integer()
    Curveball = fields.Integer()
    Changeup = fields.Integer()
    Cutter = fields.Integer()
    Control = fields.Integer()
    Hit = fields.Integer()
    Power = fields.Integer()
    Run = fields.Integer()
    Arm = fields.Integer()
    Field = fields.Integer()
    Overall = fields.Integer()

    @pre_dump
    def change_names(self, data, **kwargs):
        if data.get('Position'):
            data['position'] = data['Position']
        if data.get('Team'):
            data['team'] = data['Team']
        if data.get('Age'):
            data['age'] = data['Age']

        if not data['ETA'].isdigit():
            if data.get('age'):
                data['ETA'] = data['year'] + (24 - data['age'])
            else:
                del data['ETA']

        return data