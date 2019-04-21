def entry(**kwargs):
    return '\n'.join([
        "Welcome to SAMi",
        "What would you like? REPLY",
        "1 = Resources",
        "2 = Talk to a friend",
        "3 = Charge your phone",
    ])


def resources_1(**kwargs):
    return '\n'.join([
        "Welcome to resources: TEXT",
        "1 = Food",
        "2 = Shelters",
        "3 = Bathroom/Showers",
    ])


def resources_shelters_1(**kwargs):
    return '\n'.join([
        "Here are some shelters near you:",
        ""
        "Angels Flight (Youth)",
        "357 S Westlake Ave",
        "Los Angeles, California 90057",
        "0.17 miles / 0.27 kilometers",
        "(800) 833-2499",
        "5600 Rickenbacker Road",
        ""
        "Bell, California 90201",
        "(323) 263-1206",
        "0.11 miles / 0.17 kilometers",
    ])


def resources_bathrooms_1(**kwargs):
    return '\n'.join([
        "Here are some public restrooms near you:",
        "The Box La",
        "805 Traction Avenue, The Box Gallery, Los Angeles, California",
        "0.0 miles / 0.0 kilometers",
        "",
        "Staples Center",
        "1111 S Figueroa St, Los Angeles, CA Los Angeles, CA",
        "0.11 miles / 0.17 kilometers",
        "",
        "Snowya",
        "123 Astronaut E S Onizuka St, Los Angeles, California",
        "0.17 miles / 0.27 kilometers",
    ])
