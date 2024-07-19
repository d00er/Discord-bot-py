def server_schema(server) -> dict:
    return {"id": server["id"],
            "prefix": server["prefix"],
            "mute_role": server["mute_role"],
            "level_channel": server["level_channel"],
            "shop": server["shop"],
            "channelW": server["channelW"],
            "messageW": server["messageW"],
            "autoroleW": server["autoroleW"],
            "imageurlW": server["imageurlW"],
            "channelG": server["channelG"],
            "messageG": server["messageG"],
            "autoroleG": server["autoroleG"],
            "imageurlG": server["imageurlG"]}

def user_schema(user) -> dict:
    return {"id": user["id"],
            "level": user["level"],
            "experience": user["experience"],
            "balance": user["balance"],
            "deposite": user["deposite"],
            "objects": user["objects"]}


