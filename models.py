from django.db import models
from django.utils import timezone


#class VictimQuerySet(models.QuerySet):
#    def authors(self):
#        return self.filter(role='A')


class Victim(models.Model):
    host_name = models.CharField(max_length=200)
    internal_ip = models.GenericIPAddressField(null=True, blank=True)
    external_ip = models.GenericIPAddressField(null=True, blank=True)
    current_user = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    admin = models.BooleanField()
    last_beacon = models.DateTimeField(auto_now=True)

#    on_stack = VictimQuerySet.as_manager()

    @classmethod
    def from_beacon(cls, beacon):
        return Victim(host_name=beacon.host_name,
                      internal_ip=beacon.internal_ip,
                      external_ip=beacon.external_ip,
                      current_user=beacon.current_user,
                      os=beacon.os,
                      admin=(beacon.admin == 'Y'))

    def __str__(self):
        return '/'.join((self.host_name,
                         str(self.internal_ip),
                         str(self.external_ip),
                         self.current_user,
                         self.os,
                         str(self.admin),
                         str(self.last_beacon)))


class Command(models.Model):
    SLEEP = 'SLEP'
    OPENSSH = 'OSSH'
    CLOSESSH = 'CSSH'
    OPENTCP = 'OTCP'
    CLOSETCP = 'CTCP'
    OPENDYN = 'ODYN'
    CLOSEDYN = 'CDYN'
    TASK = 'TASK'
    
    COMMAND_TYPES = (
        (SLEEP, 'Sleep'),
        (OPENSSH, 'OpenSSHTunnel'),
        (CLOSESSH, 'CloseSSHTunnel'),
        (OPENTCP, 'OpenTCPTunnel'),
        (CLOSETCP, 'CloseTCPTunnel'),
        (OPENDYN, 'OpenDynamic'),
        (CLOSEDYN, 'CloseDynamic'),
        (TASK, 'Task'),
    )

    ADDED = 'A'
    SENT= 'S'
    SUCC = 'V'
    FAIL = 'F'

    COMMAND_STATUS = (
        (ADDED, 'Added'),
        (SENT, 'Sent'),
        (SUCC, 'Success'),
        (FAIL, 'Failed'),
    )

    victim = models.ForeignKey(Victim, on_delete=models.CASCADE)
    command_type = models.CharField(max_length=4, choices=COMMAND_TYPES)
    command_param = models.CharField(max_length=500, blank=False)  # can be blank! close commands don't need a parameter
    status = models.CharField(max_length=1, choices=COMMAND_STATUS, default=ADDED)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '///'.join((self.victim.host_name,
                           self.command_type,
                           self.command_param,
                           str(self.timestamp),
                           self.status))
