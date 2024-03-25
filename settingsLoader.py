import json

def load_settings():
    with open("settings.json", "r") as file:
        return json.load(file)

def reset_to_default():
    with open("defaultSettings.json", "r") as file:
        default_settings = json.load(file)

    with open("settings.json", "w") as file:
        json.dump(default_settings, file, indent=4)

def save_settings(volume, sound_effects):
    with open("settings.json", "r") as file:
        settings = json.load(file)
    settings['VOLUME'] = volume
    settings['SOUND_EFFECTS'] = sound_effects
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)