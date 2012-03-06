from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from give.models import *

from collections import namedtuple

import simplejson as json

from _common import render_to_response2

API_LOGIN_URL=settings.LOGIN_URL

_FORMAT_LIST = ['json']

class _apicall(object):
    def __init__(self):
        self.apiview = None

    def set_format(self, *args, **kwargs):
        Format = namedtuple('Format', 'resp_encode resp_mimetype req_decode')
        if 'format' != self.apiview.func_code.co_varnames[0]:
            raise ValueError("'%s' is no apicall. Needs argument 'format' as first argument." % \
                    self.abiview.__name__)
        if 'format' in kwargs:
            format = kwargs.pop('format')
        else:
            format = 'json'
        if format not in _FORMAT_LIST:
            raise Http404
        if format == 'json':
            form = Format(json.dumps, 'application/json', json.loads)
        args = tuple([form] + list(args))
        return self.apiview(*args,**kwargs)

    def __call__(self, apiview):
        self.apiview = apiview
        return self.set_format

def _respond(
        ResponseObjectType=HttpResponse, 
        content=None, 
        mimetype=None,
        content_type=settings.DEFAULT_CONTENT_TYPE
    ):
    return ResponseObjectType(
            content=content,
            mimetype=mimetype,
            content_type=content_type
        )

def api_doc(request):
    return render_to_response2(request, 'give/api.html')

@login_required(login_url=API_LOGIN_URL)
@_apicall()
def get_history(format, request):
    history = {}
    profile = get_object_or_404(DataloveProfile, pk=request.user.id)
    #history['send'] = common.get_history(sender=profile)
    #history['received'] = common.get_history(recipient=profile)
    return _respond(
            content=format.resp_encode(history)
        )

@_apicall()
def profile(format, request, username):
    profile = get_object_or_404(DataloveProfile,user__username=username)
    selection = ['username','received_love','websites']
    if request.user.is_authenticated() and request.user == profile.user:
        selection += ['available_love']
    return _respond(
            content=format.resp_encode(profile.get_profile_dict(selection))
        )
