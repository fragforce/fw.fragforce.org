from django.db import models
import uuid
from django.contrib import admin

### Ports ###
class TUPort(models.Model):
    PROTO_TCP = 'tcp'
    PROTO_UDP = 'udp'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=False, null=False, blank=False, help_text="Port common name")
    proto = models.CharField(max_length=3, null=False, default=PROTO_TCP, help_text="IP Protocol",
                             choices=((PROTO_TCP, 'TCP'), (PROTO_UDP, 'UDP')))
    port = models.IntegerField(null=False, default=None, help_text="TCP or UDP port number")


admin.site.register(TUPort)

class PortGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, help_text="Port group name")
    description = models.TextField(null=False, blank=True, help_text="Extended details")
    # All ports in this group
    ports = models.ManyToManyField(TUPort)


admin.site.register(PortGroup)

### Firewalls ###

class FirewallHardwareClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, help_text="Hardware Class Name")
    description = models.TextField(null=False, blank=True, help_text="Extended details")


admin.site.register(FirewallHardwareClass)

class FirewallHardware(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, help_text="Hardware Name")
    description = models.TextField(null=False, blank=True, help_text="Extended details")
    hwclass = models.ForeignKey(FirewallHardwareClass, null=False, help_text="Base hardware", on_delete=models.CASCADE)

    one_gbe_interface_count = models.IntegerField(null=True, default=None, help_text="Number of 1GbE interfaces")
    ten_gbe_interface_count = models.IntegerField(null=True, default=None, help_text="Number of 10GbE interfaces")

    ram_gb = models.IntegerField(null=True, default=None, help_text="Amount of installed RAM in GiB")


admin.site.register(FirewallHardware)

class Firewall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hw = models.ForeignKey(FirewallHardware, null=False, help_text="Base hardware", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, help_text="Asset Name")
    hostname = models.CharField(max_length=4096, unique=True, null=False, blank=False, help_text="Asset hostname")
    description = models.TextField(null=False, blank=True, help_text="Extended details")
    asset_tag = models.CharField(max_length=4096, unique=True, null=False, blank=False, help_text="Asset tag")
    org_asset_tag = models.CharField(max_length=18, unique=True, null=False, blank=False,
                                     help_text="Asset id from salesforce org's asset object")


admin.site.register(Firewall)

class LogicalFWInterface(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ifname = models.CharField(max_length=255, unique=False, null=False, blank=False, help_text="Interface name")
    ip = models.GenericIPAddressField(unique=False, null=False, blank=False, help_text="IPv4 Address")
    netmask = models.GenericIPAddressField(unique=False, null=False, blank=False, default=None,
                                           help_text="Interface's netmask")
    ip = models.GenericIPAddressField(unique=False, null=False, blank=False, help_text="IPv4 Address")
    firewall = models.ForeignKey(Firewall, null=False, help_text="Firewall this interface belongs to",
                                 on_delete=models.CASCADE)


admin.site.register(LogicalFWInterface)
