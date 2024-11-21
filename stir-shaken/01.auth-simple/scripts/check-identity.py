import sys
import json
from opensips.mi import OpenSIPSMI
import os
import importlib
import subprocess


mi_type = os.getenv('MI_TYPE', 'http')
mi_ip = os.getenv('MI_IP', '127.0.0.1')
mi_port = os.getenv('MI_PORT', '8888')


if mi_type == 'http':
    handler = OpenSIPSMI(conn='http', url='http://{}:{}/mi'.format(mi_ip, mi_port))
elif mi_type == 'datagram':
    handler = OpenSIPSMI(conn='datagram', datagram_ip=mi_ip, datagram_port=mi_port)
else:
    sys.exit(1)


def install_and_import(package, import_name=None):
    try:
        module = importlib.import_module(import_name if import_name else package)
        print(f"{package} is already installed")
    except ImportError:
        print(f"{package} is not installed, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} installed successfully")
        module = importlib.import_module(import_name if import_name else package)
    return module


def check_list(list, id, log):
    try:
        print("key %s is %s" % (log, list[id].split('=')[1]))
        return list[id].split('=')[1]
    except Exception as e:
        print("%s is not present" % log)
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    jwt = install_and_import("PyJWT", "jwt")

    dialogs = handler.execute("dlg_list_ctx")['Dialogs']
    json_dlg = json.loads(json.dumps(dialogs))
    # catch identity header in dialogs
    identity_cache = json_dlg[0]['context']['values'][0]['identity_cache']
    # Clean Identity data
    identity_cache = identity_cache.replace("Identity: ", "").replace("\\r\\n", "")
    identity_cache_list = identity_cache.split(";")

    try:
        jwt_data = identity_cache_list[0]
        jwt_decoded = jwt.decode(jwt_data, options={"verify_signature": False})
        print("jwt is decoded")
        print(jwt_decoded)
    except Exception as e:
        print("Impossible to decode JWT")
        print(e)
        sys.exit(1)

    # info=<https://certs.example.org/cert.pem>
    info = check_list(identity_cache_list, 1, "info")
    # alg=ES256
    alg = check_list(identity_cache_list, 2, "alg")
    # ppt=shaken
    ppt = check_list(identity_cache_list, 3, "ppt")

    # detect if keys are present into JWT
    jwt_keys = ["attest", "dest", "iat", "orig", "origid"]

    for key in jwt_keys:
        if key not in jwt_decoded:
            print("key %s not in jwt" % key)
            print(jwt_decoded)
            sys.exit(1)


    sys.exit(0)