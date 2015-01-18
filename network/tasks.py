from check_in.celery import app

from network.models import Switch

@app.task
def change_mac_vlan(mac, vlan):
    # Do work here

    # return result

    return True