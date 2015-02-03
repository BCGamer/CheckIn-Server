from network.providers.cisco.provider import CiscoSwitchBackend
from network.providers import registry

class CiscoCatalyst2950(CiscoSwitchBackend):
    id = 'Cisco_Catalyst_2950'
    name = 'HP Catalyst 2950'

registry.register(CiscoCatalyst2950)