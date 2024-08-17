def GetProfile(object_name):
    try:
        dict_new = [
            {
                "fullName": profile.fullName,
                "email": profile.email,
                "phone": profile.phone,
                "avatar": {
                    "alt": profile.alt,
                    "src": profile.src.url,
                },
            }
            for profile in object_name
        ]

    except ValueError:
        dict_new = [
            {
                "fullName": profile.fullName,
                "email": profile.email,
                "phone": profile.phone,
                "avatar": {
                    "alt": profile.alt,
                },
            }
            for profile in object_name
        ]

    return dict_new[0]
