# -*- coding: utf-8 -*-
# TEMPLATE of a notifications submod for the Android port of Monika After Story.
#
# What to change to make it yours is in the README. Short version:
#   1. Rename the folder and the three files, the file names have to be unique
#   2. Change the Submod(...) block and the SubmodUpdater(...) block
#   3. Replace "my_notifs" with your own module name (search and replace)
#   4. Write your messages in my_notifications_messages.rpy
#
# Settings are saved in config.json, next to this file

init -990 python in mas_submod_utils:
    Submod(
        author="YOUR NAME",
        name="My Notifications",
        description=_("A short description of what this submod does."),
        version="1.0.0",
        settings_pane="my_notifs_settings"
    )

#Updates through the Submod Updater Plugin. It is optional: without it the submod works the same
#NOTE: the tag of each release on GitHub has to be the version above (e.g. 1.0.0, the v is ignored)
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="My Notifications",
            user_name="YOUR_GITHUB_USER",
            repository_name="YOUR_REPOSITORY",
            tag_formatter=lambda tag: tag.lstrip("vV")
        )

init -5 python in my_notifs:
    import io
    import json
    import os
    import store

    #START: Paths
    def _findSubmodDir():
        """
        Finds this submod's folder, so it still works if the player renames it

        OUT:
            folder relative to the Monika After Story folder (e.g. "game/Submods/My Notifications")
        """
        for filename in renpy.list_files():
            filename = filename.replace("\\", "/")
            if filename.endswith("/my_notifications.rpy") or filename.endswith("/my_notifications.rpyc"):
                return "game/" + os.path.dirname(filename)

        return "game/Submods/My Notifications"

    SUBMOD_DIR = _findSubmodDir()
    CONFIG_PATH = os.path.join(renpy.config.basedir, SUBMOD_DIR, "config.json")

    def getImage(name):
        """
        Gets the image_path of one of this submod's avatars

        IN:
            name - avatar name (e.g. "avatar")

        OUT:
            image_path, relative to the Monika After Story folder
        """
        return "{0}/notif/{1}.png".format(SUBMOD_DIR, name)

    #START: Config
    CONFIG_VERSION = 1

    #Setting -> default value
    DEFAULT_CONFIG = {
        "shopping_minutes": 30,
        "holidays_enabled": True,
    }

    #Setting -> values the player can pick
    CONFIG_OPTIONS = {
        "shopping_minutes": [15, 30, 45, 60, 90, 120],
    }

    config = dict(DEFAULT_CONFIG)

    def loadConfig():
        """
        Loads config.json. Missing or invalid values use the defaults
        """
        global config
        config = dict(DEFAULT_CONFIG)

        if not os.path.isfile(CONFIG_PATH):
            saveConfig()
            return

        try:
            with io.open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
                data = json.load(config_file)

        except Exception as e:
            store.mas_utils.mas_log.error("[My Notifications] Failed to read config.json, using defaults: {}".format(e))
            return

        #NOTE: no isinstance(data, dict), in Ren'Py dict is RevertableDict and json returns a plain dict
        if not hasattr(data, "get"):
            return

        for key, default in DEFAULT_CONFIG.items():
            value = data.get(key)
            if isinstance(default, bool):
                if isinstance(value, bool):
                    config[key] = value

            elif value in CONFIG_OPTIONS.get(key, ()):
                config[key] = value

    def saveConfig():
        """
        Saves config.json. It's written to a temp file first, so a crash
        while saving can't leave a broken file
        """
        data = dict(config)
        data["version"] = CONFIG_VERSION
        temp_path = CONFIG_PATH + ".tmp"

        try:
            with io.open(temp_path, "w", encoding="utf-8") as config_file:
                config_file.write(unicode(json.dumps(data, indent=4, sort_keys=True)))

            #os.rename can't replace files on Windows
            if os.name == "nt" and os.path.exists(CONFIG_PATH):
                os.remove(CONFIG_PATH)
            os.rename(temp_path, CONFIG_PATH)

        except Exception as e:
            store.mas_utils.mas_log.error("[My Notifications] Failed to save config.json: {}".format(e))

    def toggleSetting(key):
        """
        Toggles a boolean setting, saves it and applies it

        IN:
            key - setting to toggle
        """
        config[key] = not config[key]
        saveConfig()
        registerNotifs()
        renpy.restart_interaction()

    def cycleSetting(key, step):
        """
        Moves a setting to the previous or next value the player can pick, saves it and applies it

        IN:
            key - setting to change
            step - -1 for the previous value, 1 for the next one
        """
        options = CONFIG_OPTIONS[key]
        index = options.index(config[key]) if config[key] in options else 0
        config[key] = options[max(0, min(len(options) - 1, index + step))]
        saveConfig()
        registerNotifs()
        renpy.restart_interaction()

    def formatMinutes(minutes):
        """
        Formats minutes for the settings screen (e.g. 90 -> "1 h 30 min")
        """
        if minutes >= 60:
            if minutes % 60:
                return "{0} h {1} min".format(minutes // 60, minutes % 60)
            return "{0} h".format(minutes // 60)

        return "{0} min".format(minutes)

    #START: Registration
    HOLIDAY_ID_PREFIX = "my_notifs_"

    def _isSupported():
        """
        Checks if this MAS can show notifications. Only the Android port has the functions of the
        notification framework, on PC (or an old port) the submod stays quiet instead of failing
        """
        return (
            renpy.android
            and hasattr(store, "mas_register_farewell_notification")
            and hasattr(store, "mas_register_holiday_notification")
        )

    def registerNotifs():
        """
        Registers all the notifications of this submod using the current settings
        """
        if not _isSupported():
            return

        #A notification sent some time after the player leaves with a farewell.
        #The label is the eventlabel of the farewell, the delay is in seconds
        #Add more farewells here, the full list of labels is in MAS (script-farewells.rpy)
        store.mas_register_farewell_notification(
            "bye_going_shopping",
            MESSAGES["shopping"],
            config["shopping_minutes"] * 60,
            image_path=getImage("avatar")
        )

        #A notification sent on a date, every year
        holiday_id = HOLIDAY_ID_PREFIX + "christmas"
        if config["holidays_enabled"]:
            store.mas_register_holiday_notification(
                holiday_id,
                MESSAGES["christmas"],
                month=12,
                day=25,
                hour=0,
                minute=0,
                image_path=getImage("avatar"),
                alarm=True
            )

        else:
            store.mas_holiday_notif_db.pop(holiday_id, None)

init 5 python in my_notifs:
    loadConfig()
    registerNotifs()

#START: Settings screen
#Shown in the Submods menu. On PC the controls are disabled, the notifications only work on Android
screen my_notifs_settings():
    vbox:
        box_wrap False
        xfill True
        xmaximum 1000
        style_prefix "check"

        if not renpy.android:
            text _("These notifications only work on Android.") text_align 0.0

        textbutton _("Holiday notifications"):
            action Function(store.my_notifs.toggleSetting, "holidays_enabled")
            selected store.my_notifs.config["holidays_enabled"] and renpy.android
            sensitive renpy.android

        hbox:
            spacing 10

            textbutton "<":
                style "check_button"
                text_style "check_button_text"
                foreground None
                padding (8, 4, 8, 4)
                action Function(store.my_notifs.cycleSetting, "shopping_minutes", -1)
                sensitive renpy.android

            text store.my_notifs.formatMinutes(store.my_notifs.config["shopping_minutes"]):
                style "confirm_prompt_text"
                yalign 0.5
                min_width 140

            textbutton ">":
                style "check_button"
                text_style "check_button_text"
                foreground None
                padding (8, 4, 8, 4)
                action Function(store.my_notifs.cycleSetting, "shopping_minutes", 1)
                sensitive renpy.android

            text _("Time after going shopping"):
                style "confirm_prompt_text"
                text_align 0.0
                yalign 0.5
