from opensipscli import cli
import jwt
import sys
import json

handler = cli.OpenSIPSCLI()


def check_list(list, id, log):
    try:
        print("key %s is %s" % (log, list[id].split('=')[1]))
        return list[id].split('=')[1]
    except Exception as e:
        print("%s is not present" % log)
        print(e)
        sys.exit(1)


if __name__ == "__main__":

    dialogs = handler.mi("dlg_list_ctx")['Dialogs']
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