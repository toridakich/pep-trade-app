from marshmallow import Schema, fields, pre_dump, post_dump

class PlayerContract(Schema):
    year = fields.Integer()
    team = fields.String()
    player = fields.String()
    length = fields.Integer()
    value = fields.Integer()
    free_agent_year = fields.Integer()

    @pre_dump
    def types(self, data, **kwargs):
        # new_data = []
        # print(data)
        # for player in data:
        #     del player['pos']
        #     del player['age']
        #     del player['contract_this_year']
        #     del player['contract_next_year']
        #     del player['contract_in_two_years']
        #     del player['contract_in_three_years']
        #     del player['contract_in_four_years']
        #     new_data.append(player)
        #     player['value'] = player['contract_value']
        #     player['length'] = player['contract_length']
        #     del player['contract_value']
        #     del player['contract_length']
        #     print(player.keys())
        # return new_data
        data['value'] = data['contract_value']
        data['length'] = data['contract_length']
        if data['free_agent_year'] == '-':
            data['free_agent_year'] = 0
        if data['value'] > 1000000000:
            data['value'] = data['value']/ 1000000
        return data
    