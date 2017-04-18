from flask import abort

# Just some fake data to play with
VALID_OS = ['osx',
            'windows',
            'linux',
            'android',
            'ios'
            ]

named_users = {
    "user-id-5678": {
        "named_user_id": "user-id-5678",
        "tags": {
            "crm": ["tag3", "tag4"]
        },
        "channels": [
            {
                "channel_id": "EFGH",
                "device_type": "ios",
                "installed": True,
                "opt_in": True,
                "push_address": "FFFF",
                "created": "2013-08-08T20:41:06",
                "last_registration": "2014-05-01T18:00:27",
                "alias": "yyyy",
                "tags": ["efgh"],
                "ios": {
                    "badge": 0,
                    "quiettime": {
                        "start": "22:00",
                        "end": "06:00"
                    },
                    "tz": "America/Los_Angeles"
                }
            }
        ]
    },
    "user-id-7890": {
        "named_user_id": "user-id-7890",
        "tags": {
            "crm": ["tag5", "tag6"]
        },
        "channels": [
            {
                "channel_id": "IJKL",
                "device_type": "osx",
                "installed": True,
                "opt_in": True,
                "push_address": "FFFF",
                "created": "2013-08-08T20:41:06",
                "last_registration": "2014-05-01T18:00:27",
                "alias": "zzzz",
                "tags": ["ijkl"],
                "ios": {
                    "badge": 0,
                    "quiettime": {
                        "start": "22:00",
                        "end": "06:00"
                    },
                    "tz": "America/Los_Angeles"
                }
            }
        ]
    },
    "user-id-1234": {
        "named_user_id": "user-id-1234",
        "tags": {
            "crm": ["tag1", "tag2"]
        },
        "channels": [
            {
                "channel_id": "ABCD",
                "device_type": "ios",
                "installed": True,
                "opt_in": True,
                "push_address": "FFFF",
                "created": "2013-08-08T20:41:06",
                "last_registration": "2014-05-01T18:00:27",
                "alias": "xxxx",
                "tags": ["asdf"],
                "ios": {
                    "badge": 0,
                    "quiettime": {
                        "start": "22:00",
                        "end": "06:00"
                    },
                    "tz": "America/Los_Angeles"
                }
            }
        ]
    }
}

CHANNELS = {
    'ABCD': 'user-id-1234',
    'IJKL': 'user-id-7890',
    'EFGH': 'user-id-5678'
}


def remove_channel_from_user(channel_id):
    user = CHANNELS[channel_id]
    new_channels = [x for x in named_users[user]['channels'] if not x['channel_id'] == channel_id]
    named_users[user]['channels'] = new_channels
    del CHANNELS[channel_id]
    return


def get_page(start_page):
    users = sorted(named_users.keys())
    if not users:
        return {}, ''

    start_page = start_page if start_page else users[0]
    if len(users) <= users.index(start_page) + 1:
        next_page = ''
    else:
        next_page = users[users.index(start_page) + 1]

    return named_users[start_page], next_page


def get(user_id):
    return named_users[user_id] if user_id in named_users else {}


def associate(channel_id, device_type, named_user_id):
    if named_user_id not in named_users or device_type not in VALID_OS:
        abort(400, 'Invalid username or os.')

    # This would likely use different functions that already exist, but adding it in here.
    if channel_id in CHANNELS:
        remove_channel_from_user(channel_id)

    user = named_users[named_user_id]
    if len(user['channels']) >= 20:
        abort(400, 'User cannot exceed 20 associated channels.')

    user['channels'].append({
        'channel_id': channel_id,
        'device_type': device_type
    })
    named_users[named_user_id]['channels'] = user['channels']
    CHANNELS[channel_id] = named_user_id
    return


def disassociate(channel_id, device_type):
    # Without knowing a little more about the underlying structure, device_type is unused
    if channel_id not in CHANNELS:
        abort(400, 'Invalid channel_id.')
    remove_channel_from_user(channel_id)
    return
