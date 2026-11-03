# MAS Submod Notifications Template

A starting point to make your own **notifications submod** for the Android port of Monika After Story (MAS).

It is a small submod that already works: it sends one notification after the player says goodbye to go shopping, and one on Christmas. It has a settings screen, a `config.json`, an example of translation and support for [Submod Updater Plugin](https://github.com/Booplicate/MAS-Submods-SubmodUpdaterPlugin). You change the names, the messages and the times, and it is yours.

The official submod, [Android Notifications](https://github.com/The-Encoders-Club/NotifSubmodTemplate), is a full example of the same idea (many farewells, holidays, interactive notifications with replies and follow-ups, and app reactions).

> [!NOTE]
> Notifications only work in the **Android port** of MAS. On PC the submod loads and stays quiet: its settings show a note and the controls are disabled.

---

## What is in the box

```
My Notifications/
├── my_notifications.rpy            the submod: registration, settings, config and the updater
├── my_notifications_messages.rpy   the messages of every notification
├── notif/
│   └── avatar.png                  the image shown in the notification
└── tl/
    └── your_language/
        └── my_notifications_translation.rpy  an example of how to translate it
```

---

## Make your own submod

1. **Create your repository** with the green **Use this template** button of this page.
2. **Rename the folder** `My Notifications` and the three files (`my_notifications*.rpy`). The names of the files have to be **unique**: another submod with the same file name would clash with yours. A prefix with the name of your submod is enough.
3. In the main `.rpy` file:
   - **`Submod(...)`**: change `author`, `name`, `description` and `version`.
   - **`SubmodUpdater(...)`**: change `submod` (the same text as `name`), `user_name` and `repository_name` (your GitHub user and repository). Without this the updater would look for new versions in the wrong place.
   - **`_findSubmodDir`**: change the file name it looks for.
   - **`my_notifs`**: it is the name of the module. Search and replace it with your own (for example `cool_notifs`) in the three `.rpy` files and in the screen names. If two submods use the same module name, they overwrite each other.
4. **Write your messages** in `my_notifications_messages.rpy`. Every message goes inside `_("...")`. A notification picks one at random, and you can use `[player]`. A category can also be a dict of affection level (`"broken"`, `"distressed"`, `"upset"`, `"normal"`, `"happy"`, `"affectionate"`, `"enamored"`, `"love"`) to a list, so Monika sounds different depending on how she feels.
5. **Choose when they are sent** in `registerNotifs()`:
   - `mas_register_farewell_notification(label, messages, delay_seconds, ...)`: sent some time after the player leaves with that farewell. `label` is the eventlabel of the farewell in MAS (`script-farewells.rpy`).
   - `mas_register_holiday_notification(id, messages, month=, day=, hour=, minute=, ...)`: sent on a date. For dates that depend on the player (birthdays, anniversaries) pass `date_func=` instead of month and day.
   - Useful options: `is_interactive=True` adds a **Reply** button and follow-up messages, `image_path=` sets the avatar, and `alarm=True` makes it behave like an alarm so some phones do not silence it while the screen is off (use it for long absences, like work or sleep).
6. **Avatars**: put your PNG files in `notif/` and use `getImage("name")`. A notification without an image uses the icon of the app.
7. **Translate** it: the example is in `tl/your_language/`. Rename the folder to the name of your language in the game (for example `tl/spanish/`), change `translate your_language strings:` to the same name, and write every `new` line. The `old` lines have to match the English text exactly. Until you do it the file does nothing.

### Good to know

> [!IMPORTANT]
> The names of the files have to be **unique**. Another submod with a file called `notifications.rpy` would clash with yours, so give every file the prefix of your submod.

> [!WARNING]
> **Keep the check `_isSupported()`.** The notification functions only exist in the Android port. Without it your submod would fail on PC.

> [!NOTE]
> The game runs on **Ren'Py 6 and Python 2.7**: no f-strings. Use `"{0}".format(...)`.

> [!TIP]
> Do not use `persistent` for the settings of your submod. Keep them in its own `config.json`, like this template does.

- **Do not edit other submods.** If something does not work with another one, tell its author or us.
- When you open the game, the farewell notifications that were still pending are cancelled. The holiday ones are cancelled only if it is that very day.

---

## Test it without waiting

Notifications are sent after minutes or hours. To test quickly, change `config["shopping_minutes"] * 60` in `registerNotifs()` to something like `15` (15 seconds), say goodbye with "going shopping" and leave the game.

> [!CAUTION]
> Put the real time back before you publish the submod, or your players will get the test notifications after seconds.

---

## Publish a version

1. Raise `version` in the `Submod(...)` block.
2. Make a zip that contains the whole folder of your submod (`.rpy` files, `notif/` and `tl/`; **without** `config.json` or `.rpyc` files).
3. On GitHub, create a **Release** whose **tag is the same as the version** (for example `1.0.1`; a `v` in front is ignored) and attach the zip as the **only file**. That is what Submod Updater Plugin downloads.
4. The plugin checks GitHub at most once an hour.

> [!IMPORTANT]
> The **tag of the release has to match the `version`** of the `Submod(...)` block (a `v` in front is ignored). If they differ, the plugin will keep offering an update that does not exist.

---

## Community

Questions, bugs or ideas? Join the [The Encoders Club Discord server](https://discord.com/servers/the-encoders-club-1191061790835093564).

---

## License

MIT. Copyright (c) 2026 The Encoders Club.
