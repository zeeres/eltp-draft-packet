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
            'weekly': [w1, w2, w3, w4, w5, w6, w7,
                       w8, w9, w10, w11, w12, w13, w14],
            'daily': [monday, tuesday, wednesday, thursday,
                      friday, saturday, sunday],
            'comment': comment_availability
        },

        'position': {
            'primary': position,
            'preference': position_preference
        },

        'microphone': microphone,

        'comment': comment
    }


reddit_regex = re.compile(r'(/?u/)?(.*)')


def fix_reddit(name):
    m = reddit_regex.match(name)

    if m is not None:
        return m.group(2)

    return name  # Oh well
