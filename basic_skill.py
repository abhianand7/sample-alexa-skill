
from __future__ import print_function
import datetime
from datetime import date

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome, you can use me to ask me for prayer times, "\
                    "say, 'help', to know more about what I can do"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "what else would you like to know?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using me "\
                    "have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


# def set_color_in_session(intent, session):
#     """ Sets the color in the session and prepares the speech to reply to the
#     user.
#     """
#
#     card_title = intent['name']
#     session_attributes = {}
#     should_end_session = False
#
#     if 'Color' in intent['slots']:
#         favorite_color = intent['slots']['Color']['value']
#         session_attributes = create_favorite_color_attributes(favorite_color)
#         speech_output = "I now know your favorite color is " + \
#                         favorite_color + \
#                         ". You can ask me your favorite color by saying, " \
#                         "what's my favorite color?"
#         reprompt_text = "You can ask me your favorite color by saying, " \
#                         "what's my favorite color?"
#     else:
#         speech_output = "I'm not sure what your favorite color is. " \
#                         "Please try again."
#         reprompt_text = "I'm not sure what your favorite color is. " \
#                         "You can tell me your favorite color by saying, " \
#                         "my favorite color is red."
#     return build_response(session_attributes, build_speechlet_response(
#         card_title, speech_output, reprompt_text, should_end_session))


# def get_color_from_session(intent, session):
#     session_attributes = {}
#     reprompt_text = None
#
#     if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
#         favorite_color = session['attributes']['favoriteColor']
#         speech_output = "Your favorite color is " + favorite_color + \
#                         ". Goodbye."
#         should_end_session = True
#     else:
#         speech_output = "I'm not sure what your favorite color is. " \
#                         "You can say, my favorite color is red."
#         should_end_session = False
#
#     # Setting reprompt_text to None signifies that we do not want to reprompt
#     # the user. If the user does not respond or says something that is not
#     # understood, the session will end.
#     return build_response(session_attributes, build_speechlet_response(
#         intent['name'], speech_output, reprompt_text, should_end_session))
# d0 = date.today()
# d1 = datetime.datetime.strptime('2016-10-29', '%Y-%m-%d')
# d1 = date(d1.year, d1.month, d1.day)
# print ((d1 - d0).days)


def time_method(query):
    today = date.today()
    today_day = today.strftime('%A').lower()
    if query:
        query_date = datetime.datetime.strptime(query, '%Y-%m-%d')
        query_day = query_date.strftime('%A').lower()
        query_date_date = date(query_date.year, query_date.month, query_date.day)
        delta = (query_date_date - today).days
    else:
        query_day = today_day
        delta = 0
    return query_day, today_day, delta


def handle_query(intent, time_log, prayer):
    try:
        query_date = intent['slots']['day']['value']
    except:
        query_date = ''
    query_day, today, delta = time_method(query_date)
    if query_day == today:
        prayer_time = time_log[query_day]
        query_day = 'today'
    else:
        # from time delta get the days apart
        # if day apart is 1, make query_day = 'tomorrow'
        # otherwise, make the query_day = 'on next {0}'.format(query_day)
        prayer_time = time_log[query_day]
        if delta == 1:
            query_day = 'on tomorrow'
        else:
            query_day = 'on {0}'.format(query_day)
    session_attributes = {}
    reprompt_text = None
    should_end_session = False
    output_text = "{0} at {1} {2}".format(prayer, prayer_time.replace(':', ' '), query_day)

    return build_response(session_attributes, build_speechlet_response(intent['name'], output_text,
                                                                       reprompt_text, should_end_session))


# below methods will fetch the correct day reffered by the user and correspondingly will fetch the time of that day
def handle_fajr_start(intent, session):
    fajr_start = {'sunday': '5:17', 'monday': '5:18', 'tuesday': '5:21',
                    'wednesday': '5:23', 'thursday': '5:24', 'friday': '5:27',
                    'saturday': '5:28'}
    return handle_query(intent, fajr_start, 'Fajr, starts')


def handle_fajr_jamat(intent, session):
    fajr_jamat = {'sunday': '5:47', 'monday': '5:48', 'tuesday': '5:51',
                  'wednesday': '5:53', 'thursday': '5:54', 'friday': '5:57',
                  'saturday': '5:57'}
    return handle_query(intent, fajr_jamat, 'Fajr Jamat is')


def handle_fajr_end(intent, session):
    fajr_end = {'sunday': '6:46', 'monday': '6:47', 'tuesday': '6:49',
                  'wednesday': '6:51', 'thursday': '6:52', 'friday': '6:54',
                  'saturday': '6:55'}
    return handle_query(intent, fajr_end, 'Fajr, ends')


def handle_zuhor_start(intent, session):
    zuhor_start = {'sunday': '12:58', 'monday': '12:57', 'tuesday': '12:57',
                  'wednesday': '12:57', 'thursday': '12:56', 'friday': '12:56',
                  'saturday': '12:56'}
    return handle_query(intent, zuhor_start, 'Zuhor, starts')


def handle_zuhor_jamat(intent, session):
    zuhor_jamat = {'sunday': '1:15', 'monday': '1:30', 'tuesday': '1:30',
                  'wednesday': '1:30', 'thursday': '1:30', 'friday': '1:30',
                  'saturday': '1:30'}
    return handle_query(intent, zuhor_jamat, 'Zuhor Jamat is')


def handle_asr_start(intent, session):
    asr_start = {'sunday': '4:59', 'monday': '4:57', 'tuesday': '4:55',
                  'wednesday': '5:53', 'thursday': '4:51', 'friday': '4:49',
                  'saturday': '4:47'}
    return handle_query(intent, asr_start, 'Asr, starts')


def handle_asr_jamat(intent, session):
    asr_jamat = {'sunday': '5:15', 'monday': '5:15', 'tuesday': '5:15',
                  'wednesday': '5:15', 'thursday': '5:15', 'friday': '5:15',
                  'saturday': '5:15'}
    return handle_query(intent, asr_jamat, 'Asr Jamat is')


def handle_maghrib_start(intent, session):
    maghrib_start = {'sunday': '6:59', 'monday': '6:56', 'tuesday': '6:54',
                  'wednesday': '6:52', 'thursday': '6:50', 'friday': '6:47',
                  'saturday': '6:45'}
    return handle_query(intent, maghrib_start, 'Maghrib, starts')


def handle_maghrib_jamat(intent, session):
    maghrib_jamat = {'sunday': '7:04', 'monday': '7:01', 'tuesday': '6:59',
                  'wednesday': '6:59', 'thursday': '6:57', 'friday': '6:55',
                  'saturday': '6:52'}
    return handle_query(intent, maghrib_jamat, 'Maghrib Jamat is')


def handle_esha_start(intent, session):
    esha_start = {'sunday': '8:15', 'monday': '8:12', 'tuesday': '8:11',
                  'wednesday': '8:09', 'thursday': '8:07', 'friday': '8:04',
                  'saturday': '8:02'}
    return handle_query(intent, esha_start, 'Esha, starts')


def handle_esha_jamat(intent, session):
    esha_jamat = {'sunday': '8:30', 'monday': '8:30', 'tuesday': '8:30',
                  'wednesday': '8:30', 'thursday': '8:30', 'friday': '8:30',
                  'saturday': '8:30'}
    return handle_query(intent, esha_jamat, 'Esha Jamat is')


def handle_invalid_intent(intent, session):
    session_attributes = {}
    reprompt_text = None
    output_text = "Sorry I didn't catch that, " \
                  "Plese try saying that again"
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(intent['name'], output_text, reprompt_text, should_end_session))


def handle_stop_intent(intent, session):
    session_attributes = {}
    reprompt_text = None
    output_text = "Stopping, " \
                  "ask again, " \
                  "say cancel to exit the skill"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(intent['name'], output_text,
                                                                       reprompt_text, should_end_session))


# more intent handlers for future use
def handle_yes_intent(intent, session):
    pass


def handle_no_intent(intent, session):
    pass

def handle_start_over_intent(intent, session):
    pass


def handle_help_intent(intent, session):
    session_attributes = {}
    reprompt_text = None
    speech_output = "Glad I can be of help, " \
                    "You can ask me the prayer timings of the whole week ahead, " \
                    "trying saying, when does Fajr Jamat Starts tomorrow?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(intent['name'], speech_output,
                                                                       reprompt_text, should_end_session))


    # --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetFajrStart":
        return handle_fajr_start(intent, session)
    elif intent_name == "GetFajrJamat":
        return handle_fajr_jamat(intent, session)
    elif intent_name == "GetFajrEnd":
        return handle_fajr_end(intent, session)
    elif intent_name == "GetZuhorStart":
        return handle_zuhor_start(intent,session)
    elif intent_name == "GetZuhorJamat":
        return handle_zuhor_jamat(intent, session)
    elif intent_name == "GetAsrStart":
        return handle_asr_start(intent,session)
    elif intent_name == "GetAsrJamat":
        return handle_asr_jamat(intent, session)
    elif intent_name == "GetMaghribStart":
        return handle_maghrib_start(intent, session)
    elif intent_name == "GetMaghribJamat":
        return handle_maghrib_jamat(intent, session)
    elif intent_name == "GetEshaStart":
        return handle_esha_start(intent, session)
    elif intent_name == "GetEshaJamat":
        return handle_esha_jamat(intent,session)
    # elif intent_name == "WhatsMyColorIntent":
    #     return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help_intent(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_stop_intent(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return handle_yes_intent(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return handle_no_intent(intent, session)
    elif intent_name == "AMAZON.StartOverIntent":
        return handle_help_intent(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.StopIntent":
        return handle_stop_intent(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.ask.skill.a32143af-fb1f-450f-b9d8-7115b6a1f9c9"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
