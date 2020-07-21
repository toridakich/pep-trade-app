from marshmallow import Schema, fields, validate, pre_dump, post_dump

class TeamPayroll(Schema):
    year = fields.Integer()
    team = fields.String()
    payroll_this_year = fields.Integer()
    payroll_next_year = fields.Integer()
    payroll_in_two_years = fields.Integer()
    payroll_in_three_years = fields.Integer()
    payroll_in_four_years = fields.Integer()


    @post_dump(pass_original=True)
    def year(self, data, original_data, **kwargs):

        data['year'] = original_data['year']
        return data
        #print('year', data['year'])