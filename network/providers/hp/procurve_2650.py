from network.providers.hp.provider import HPSwitchBackend
from network.providers import registry

class HPProcurve2650(HPSwitchBackend):
    id = 'HP_Procurve_2650'
    name = 'HP Procurve 2650'

registry.register(HPProcurve2650)