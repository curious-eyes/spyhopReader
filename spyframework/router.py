#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import logging
import webapp2
import spy_setting
import re


def custom_dispatcher(router, request, response):
    route, args, kwargs = rv = router.match(request)
    request.route, request.route_args, request.route_kwargs = rv

    handler = route.handler
    if isinstance(handler, basestring):
        handler, args, kwargs = parse_handler_template(request, handler, args, kwargs)
#        logging.info('handler is %s' % handler)
#        logging.info(request.route_args)
#        logging.info(request.route_kwargs)
#        for x in request.params:
#            logging.info('Param is %s' % x)
        router.handlers[handler] = handler = webapp2.import_string(handler)
        """
        if handler not in self.handlers:
            router.handlers[handler] = handler = webapp2.import_string(handler)
        else:
            handler = router.handlers[handler]
        """

    return router.adapt(handler)(request, response)


def parse_handler_template(request, handler, args, kwargs):
    """replace {key} in `handler` with values from `args` or `kwargs`.
    Replaced values are removed from args/kwargs."""
    args = request.path[1:].split('/')

    dict_path = {}
    for index, value in enumerate(args):
        dict_path[index] = value

    module = dict_path.get(0, spy_setting.DEFAULT_MODULE)
    controller = dict_path.get(1, spy_setting.DEFAULT_CONTROLLER)
    action = dict_path.get(2, spy_setting.DEFAULT_ACTION)
    action = (action[0]).upper() + action[1:]

    kwargs = {'module': module, 'controller': controller, 'action': action}
#    logging.info(kwargs)
#    logging.info(args)
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
        return kwargs.pop(match.group().strip('{}'))

    return re.sub('{.*?}', sub, handler), args, kwargs
