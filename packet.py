import pycountry
import re


def process_row(row, rating):
    (
        timestamp, player_name, old_name, tagpro_id, reddit_name,
        country, ping_orbit, ping_chord,
        w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14,
        monday, tuesday, wednesday, thursday, friday, saturday, sunday,
        comment_availability,
        position, position_preference,
        microphone, comment,
        __, ___,
        removed,
        captain,
        restriction,
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

    captain = captain == '1'

    return {
        'name': player_name,
        'old_name': fix_old_name(old_name, player_name),
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
            'comment': comment_availability.strip()
        },

        'position': pos,

        'microphone': microphone,

        'comment': comment.strip(),

        'rating': 0 if captain else rating.get_rating(),

        'captain': captain,

        'restriction': restriction.strip(),

        'removed': removed == '1'
    }


def fix_old_name(name, new_name):
    if name.lower().strip() in ('no', 'no.', 'n/a', new_name.lower().strip()):
        return ''
    return name


reddit_regex = re.compile(r'(/?u/)?(.*)')


def fix_reddit(name):
    m = reddit_regex.match(name)

    if m is not None:
        return m.group(2)

    return name  # Oh well


def fix_country(country):
    country_ = country.lower().strip()
    c = None

    if country_ in ('the netherlands', 'dutchlandistan'):  # thanks poukie
        c = pycountry.countries.get(alpha_2='NL')

    if country_ in ('england', 'scotland', 'wales', 'northern ireland',
                    'uk', 'great britain'):
        c = pycountry.countries.get(alpha_2='GB')

    if country_ in ('us', 'usa', 'united states of america', 'america') or\
            'america' in country_ or 'murica' in country_:  # sorry
        c = pycountry.countries.get(alpha_2='US')

    if country_ == 'macedonia':
        c = pycountry.countries.get(alpha_2='MK')

    def try_find_country(c):
        # I'm so sorry
        try:
            return pycountry.countries.get(name=c)
        except KeyError:
            try:
                return pycountry.countries.get(official_name=c)
            except KeyError:
                try:
                    return pycountry.countries.get(alpha_2=c)
                except KeyError:
                    try:
                        return pycountry.countries.get(alpha_3=c)
                    except KeyError:
                        return None

    if c is None:
        c = try_find_country(country)

    if c is None:
        c = try_find_country(country_.title()
                                     .replace('And', 'and')
                                     .replace('Of', 'of'))

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

    return pos

    # pref = ''
    # if pos == '?':
    #     if preference == 'I prefer offence':
    #         pref = 'o'
    #     elif preference == 'I prefer defence':
    #         pref = 'd'

    # return {'primary': pos, 'preference': pref}


def fix_microphone(microphone):
    return microphone == 'Yes'
