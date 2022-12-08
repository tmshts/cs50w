AMENITIES_CHOICES = [
    ('Furnished', 'Furnished'),
    ('Disabled Access', 'Disabled Access'),
    ('Balcony', 'Balcony'),
    ('Garage Parking', 'Garage Parking'),
    ('Street Parking', 'Street Parking'),
    ('Air Conditioning', 'Air Conditioning'),
    ('Heating', 'Heating'),
    ('Kitchen', 'Kitchen'),
    ('Dishwasher', 'Dishwasher'),
    ('Washing Machine', 'Washing Machine'),
    ('Fridge', 'Fridge'),
    ('Freezer', 'Freezer'),
    ('Oven', 'Oven'),
    ('Dryer', 'Dryer'),
    ('TV', 'TV'),
    ('Internet', 'Internet'),
    ('Elevator', 'Elevator'),
    ('Gym', 'Gym'),
    ('Sauna', 'Sauna'),
    ('Pool', 'Pool'),
    ('Basement', 'Basement'),

]

TOTAL_BEDROOM_CHOICES = [
    ('', ''),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
]

TOTAL_BATHROOM_CHOICES = [
    ('', ''),
    (1.0, 1),
    (1.5, 1.5),
    (2.0, 2),
    (2.5, 2.5),
    (3.0, 3),
    (3.5, 3.5),
    (4.0, 4),
    (4.5, 4.5),
    (5.0, 5),
    (5.5, 5.5),
    (6.0, 6),
    (6.5, 6.5),
    (7.0, 7),
]

ORDERING_CHOICES = (
            ('-time_of_creation', ('Newest Arrivals')),
            ('time_of_creation', ('Oldest Arrivals')),
            ('price', ('Price: Low to High')),
            ('-price', ('Price: High to Low')),
            ('size', ('Size: Small to Big')),
            ('-size', ('Size Big to Small')),
        )