# services/choices.py 
# Define choices for event types with English keys and Chinese labels.

service_type_choices = [
    ('_', '類型(全部)'),
    ('Elderly', '長者'),
    ('Youth', '青年'),
    ('Family', '家庭及兒童'),
    ('Class', '興趣班'),
    ('Communities', '社區共融'),
    ('others', '其他'),
]

service_date_choices = [
    ('_', '服務日期(全部)'),
    ('1', '1天內'),
    ('3', '3天內'),
    ('7', '7天內'),
    ('14', '14天內'),
    ('30', '30天內'),
    ('90', '90天內'),
]

# service_type_choices = {
#     '_': '類型(全部)',
#     'Elderly':'長者',
#     'Youth': '青年',
#     'Family': '家庭及兒童',
#     'Class':'興趣班',
#     'Communities': '社區共融',
#     'other':'其他'    
# }