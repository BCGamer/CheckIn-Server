from django.db import models


class Switch(models.Model):

    HP_SWITCH = 'hp'
    CISCO_SWITCH = 'cisco'

    SWITCH_TYPES = (
        (HP_SWITCH, 'HP'),
        (CISCO_SWITCH, 'Cisco'),
    )


    name = models.CharField(max_length=40)
    ip = models.GenericIPAddressField()

    type = models.CharField(max_length=20, choices=SWITCH_TYPES, default=HP_SWITCH)

    class Meta:
        verbose_name_plural = 'Switches'