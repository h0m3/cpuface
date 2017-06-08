"""
    This module interfaces CPUFace with
    the Profiles Database
"""


from os import getenv, path
from json import dump, load

profiles_path = path.realpath(path.expanduser("~")+"/.cpuface_profiles.json")


def load_profiles():
    try:
        if (not(path.isfile(profiles_path))):
            buf = open(profiles_path, 'w')
            dump(dict(), buf)
            buf.close()
        buf = open(profiles_path, 'r')
        json = load(buf)
        buf.close()
        return json
    except (IOError, OSError) as err:
        print("[CPUFace] Unable to load profiles file: %s" % err.strerror)
        return dict()
    except Exception as err:
        print("[CPUFace] Unable to parse profiles file")
        return dict()


def save_profiles(profiles):
    try:
        buf = open(profiles_path, 'w')
        dump(profiles, buf)
        buf.close()
        return True
    except (IOError, OSError) as err:
        print("[CPUFace] Unable to store profiles: %s" % err.strerror)
        return False
    except Exception as err:
        print("[CPUFace] Unable to parse json, please report this.")
        return False
