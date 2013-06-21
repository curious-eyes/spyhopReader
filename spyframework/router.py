#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import logging
import webapp2
import jinja2
import spy_setting
import re


class RouterBaseHandler(webapp2.RequestHandler):
    # Module, Controller, Action
    adapted_handler_spec = {}

    def get_module_name(self):
        return self.adapted_handler_spec['module']

    def get_controller_name(self):
        return self.adapted_handler_spec['controller']

    def get_action_name(self):
        return self.adapted_handler_spec['action']


def custom_dispatcher(router, request, response):
    route, args, kwargs = rv = router.match(request)
    request.route, request.route_args, request.route_kwargs = rv

    handler = route.handler
    if isinstance(handler, basestring):
        handler, args, kwargs = parse_handler_template(request, handler, args, kwargs)
        # debug logging
        # logging.info('handler is %s' % handler)
        # logging.info(request.route_args)
        # logging.info(request.route_kwargs)
        # for x in request.params:
        #     logging.info('Param is %s' % x)
        # logging.info(args)
        # logging.info(kwargs)
        try:
            handler = webapp2.import_string(handler)
            # Module, Controller, Action 文字列格納
            handler.adapted_handler_spec = kwargs
            # jinjaテンプレート定義
            handler.JINJA_ENVIRONMENT = jinja2.Environment(
                loader=jinja2.FileSystemLoader(spy_setting.MODULES_DIR + '/' + kwargs['module'] + '/views/templates/' + kwargs['controller']),
                extensions=['jinja2.ext.autoescape'])

            router.handlers[handler] = handler
        except webapp2.ImportStringError:
            webapp2.abort(404)

    return router.adapt(handler)(request, response)


def parse_handler_template(request, handler, args, kwargs):
    """replace {key} in `handler` with values from `args` or `kwargs`.
    Replaced values are removed from args/kwargs."""
    args = request.path[1:].split('/')

    dict_path = {}
    for index, value in enumerate(args):
        if (len(value) == 0):
            continue
        dict_path[index] = value

    module = dict_path.get(0, spy_setting.DEFAULT_MODULE)
    controller = dict_path.get(1, spy_setting.DEFAULT_CONTROLLER)
    action = dict_path.get(2, spy_setting.DEFAULT_ACTION)
    action = (action[0]).upper() + action[1:]

    kwargs = {'module': module, 'controller': controller, 'action': action}
    # logging.info(kwargs)
    # logging.info(args)
    counter = 3
    while True:
        key = dict_path.get(counter, None)
        val = dict_path.get(counter+1, None)
        if key is not None:
            request.GET.add(key, val)
            counter += 2
        else:
            break

    def sub(match):
        return kwargs.get(match.group().strip('{}'))

    return re.sub('{.*?}', sub, handler), args, kwargs
