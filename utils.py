import xml.etree.ElementTree as ET
import sys
#from django.db.models.query import QuerySet

class Beacon:
    def __init__(self, raw_xml):
        xml = raw_xml.decode('utf-8')
        resp = ET.fromstring(xml)

        #if resp.find('ID') is not None and resp.find('ID').text:
        #    self.id = int(resp.find('ID').text)
        #else:
        #    self.id = 0
        self.host_name = resp.find('HostName').text
        if resp.find('InternalIP') is not None and resp.find('InternalIP').text:
            self.internal_ip = resp.find('InternalIP').text
        else:
            self.internal_ip = ''
        if resp.find('ExternalIP') is not None and resp.find('ExternalIP').text:
            self.external_ip = resp.find('ExternalIP').text
        else:
            self.external_ip = ''
        self.current_user = resp.find('CurrentUser').text
        self.os = resp.find('OS').text
        self.admin = (resp.find('Admin').text == 'Y')

    @classmethod
    def beacon_response(cls, stack):
        xml = '<beaconResponse>\n'
        xml += '\t<commands>\n'
        for i, cmd in enumerate(stack):
            xml += '\t\t<command id="{}" type="{}" param="{}"/>\n'\
                    .format(cmd.id, cmd.command_type, cmd.command_param)
        xml += '\t</commands>\n'
        xml += '</beaconResponse>'
        return xml
