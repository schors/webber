# -*- coding: utf-8 -*-
import os

import webber
from webber import set_hook, cfg, relpath, functions

from jinja2 import Environment, FileSystemLoader


@set_hook('pagetemplate')
def pagetemplate(params):
    env = Environment(loader=FileSystemLoader(os.path.join(
        os.path.dirname(webber.__file__), cfg.style_dir
    )))

    template_filename = params.file.template
    if not template_filename.endswith('.html'):
            template_filename += '.html'
    template = env.get_template(template_filename)

    kw = {
        'file': params.file,
        'body': params.file.contents,
    }
    kw.update(params.file)
    kw.update(functions)

    rendered = template.render(**kw)
    return rendered
