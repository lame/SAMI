def welcome_1() -> str:
    """
    Onboarding step 1:
        Welcome the user to the service, get consent
        from the user to start using the service and
        approval to open an account in their phone
        number.
    """
    return '''Welcome to TextHomelessHelp! TextHomelessHelp is a
    messaging service to connect you to resources for the homeless
    population. TextHomelessHelp is a free service; it is
    free to start, free to use, and will provide mental health
    resources and living resources available in your area.

    If you would like to join, please respond "JOIN" for more
    information, respond "OUT" to opt out of all future invitations,
    or simply ignore this message.
    '''


def welcome_2() -> str:
    """
    Onboarding step 2:
        Explain the service to the user, outline
        'Help' as well as other common keywords.
        Give link to the website
    """
    return '''
    Thanks for joining TextHomelessHelp. Text the word "friend"
    to open a chat with a friend and text "resources" for a list
    of local outreach and resources that can help you out. For this
    to work please answer the following questions with the most
    accurate information you can to receive help in your area.

    Let's start with your name. Please respons with your first name
    or a nickname you'd like us to call you.
    '''


def welcome_3(fname: str) -> str:
    """
    Onboarding step 3:
        Echo the name, get age
    """
    return f'''
    Hi {fname}, we're happy you joined TextHomelessHelp! To best
    assist you, please provide us with your current age
    '''


def welcome_4() -> str:
    """
    Onboarding step 4:
        We have their age, let's get their location
    """
    return f'''
    Now for us to find assistance and resources near you,
    please respond with the approximate 5 digit zip
    code of the area you're in.
    '''


def welcome_5(fname: str, county: str) -> str:
    """
    Onboarding step 5:
        We've now completed onboarding. Let's remind them of the
        commands and finish creating the profild

    FIXME:  This would be a good place to add a restart command
            if some part of the provided information is incorrect.

    FIXME:  Come up with better verbage to avoid
            "mental health professional"
    """
    return f'''
    {fname} you're all done with signup! Just as a reminder you can
    text this number with "friend" at any time to connect with a
    mental health professional, or "resources" to get a list of
    nearby showers, water, electricity, shelters, and outreach in
    your area. Text "help" if you need to retrieve the available
    functionality of TextHomelessHelp at any time.
    '''
