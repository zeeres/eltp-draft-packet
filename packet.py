import pycountry
import re


def process_row(row):
    (
        timestamp, player_name, old_name, tagpro_id, reddit_name,
        country, ping_orbit, ping_chord,
        w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14,
        monday, tuesday, wednesday, thursday, friday, saturday, sunday,
        comment_availability,
        position, position_preference,
        microphone, comment,
        *_
    ) = row

    reddit_name = fix_reddit(reddit_name)
    country = fix_country(country)

    weekly = list(map(fix_weekly, [w1, w2, w3, w4, w5, w6, w7,
                                   w8, w9, w10, w11, w12, w13, w14]))
    daily = list(map(fix_daily, [monday, tuesday, wednesday, thursday,
                                 friday, saturday, sunday]))

    pos = fix_position(position, position_preference)
    microphone = fix_microphone(microphone)

    return {
        'name': player_name,
        'old_name': old_name,
        'reddit': reddit_name,
        'profile': tagpro_id,
        'country': country,
        'ping': {
            'chord': ping_chord,
            'orbit': ping_orbit
        },

        'availability': {
            'weekly': weekly,
            'daily': daily,
            'comment': comment_availability
        },

        'position': pos,

        'microphone': microphone,

        'comment': comment
    }


reddit_regex = re.compile(r'(/?u/)?(.*)')


def fix_reddit(name):
    m = reddit_regex.match(name)

    if m is not None:
        return m.group(2)

    return name  # Oh well


def fix_country(country):
    country = country.lower().strip()

    if country == 'the netherlands':
        country = 'netherlands'

    if country in ('england', 'scotland', 'wales', 'northern ireland',
                   'uk', 'great britain'):
        country = 'united kingdom'

    if country in ('us', 'usa', 'united states of america', 'america') or\
            'america' in country:  # sorry
        country = 'united states'

    c = None
    country_ = country.title()

    # I'm so sorry
    try:
        c = pycountry.countries.get(name=country_)
    except KeyError:
        try:
            c = pycountry.countries.get(official_name=country_)
        except KeyError:
            try:
                c = pycountry.countries.get(alpha_2=country_)
            except KeyError:
                try:
                    c = pycountry.countries.get(alpha_3=country_)
                except KeyError:
                    pass

    if c is None:
        # We tried
        code = ''
        name = country
    else:
        code = c.alpha_2.lower()
        name = c.name

    return {'code': code, 'name': name}


def fix_weekly(availability):
    days = availability.split(', ')
    return ['Sunday' in days,
            'Monday' in days,
            'Tuesday' in days]


def fix_daily(availability):
    if availability == 'Definitely can\'t make it':
        return 0
    elif availability == 'I can make it':
        return 1
    elif availability == 'Would rather not play/practice':
        return 2
    else:  # Don't know
        return 3


def fix_position(position, preference):
    pos = '?'
    if position == 'Defence only':
        pos = 'd'
    elif position == 'Offence only':
        pos = 'o'

    pref = ''
    if pos == '?':
        if preference == 'I prefer offence':
            pref = 'o'
        elif preference == 'I prefer defence':
            pref = 'd'

    return {'primary': pos, 'preference': pref}


def fix_microphone(microphone):
    return microphone == 'Yes'
