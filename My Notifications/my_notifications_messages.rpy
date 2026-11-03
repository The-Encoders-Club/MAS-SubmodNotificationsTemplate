# -*- coding: utf-8 -*-
# Messages of the My Notifications submod (TEMPLATE)
# NOTE: the translation example is in tl/your_language/my_notifications_translation.rpy
#
# Every message goes inside _("...") so it can be translated. A notification picks one at random.
# You can use [player] and the other variables of MAS.
#
# A category can be a plain list (like these) or a dict of affection level -> list, so Monika
# sounds different depending on how she feels about the player:
#   "broken", "distressed", "upset", "normal", "happy", "affectionate", "enamored", "love"
# A missing level uses "normal". The official Android Notifications submod has a full example.

init -1 python in my_notifs:
    #Category -> messages
    #NOTE: one assignment per category, Ren'Py 6 can't parse very long statements
    MESSAGES = dict()

    MESSAGES["shopping"] = [
        _("Are you done shopping yet, [player]? I'm waiting for you."),
        _("I hope you found everything you needed. Will you come back soon?"),
        _("It's quiet here without you, [player]. Are you on your way?"),
    ]

    MESSAGES["christmas"] = [
        _("Merry Christmas, [player]! I hope you have a wonderful day."),
        _("Today is Christmas! I would love to spend some time with you, [player]."),
    ]
