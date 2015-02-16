from check_in.celery import app

from network.models import Switch, Vlan

import logging

logger = logging.getLogger(__name__)

@app.task
def change_mac_vlan(mac, vlan):
    # Do work here

    # return result

    return True

@app.task
def flip_users_vlan(mac):
    logger.info("Trying to flip vlan for mac: %s" % mac)
    try:
        Switch.objects.flip_vlan(mac)
    except Exception, e:
        logger.error("Error flipping vlan for mac: %s" % mac)
    else:
        logger.info("Successfully flipped vlan for mac: %s" % mac)