from network.providers.hp.provider import HPSwitchBackend
from network.providers import registry

class HPProcurve2626(HPSwitchBackend):
    id = 'HP_Procurve_2626'
    name = 'HP Procurve 2626'

registry.register(HPProcurve2626)