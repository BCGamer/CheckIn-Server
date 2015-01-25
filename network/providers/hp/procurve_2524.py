from network.providers.hp.provider import HPSwitchBackend
from network.providers import registry

class HPProcurve2524(HPSwitchBackend):
    id = 'HP_Procurve_2524'
    name = 'HP Procurve 2524'

registry.register(HPProcurve2524)