#!/usr/bin/env python
# Copyright 2013 Brett Slatkin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""App Engine configuration file.

See:
    https://developers.google.com/appengine/docs/python/tools/appengineconfig
"""

import os
import sys

# Load up our app and all its dependencies. Make the environment sane.
sys.path.insert(0, './lib/')
from dpxdt.server import app


# For debugging SQL queries.
# import logging
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


# When in production use precompiled templates.
if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    import jinja2
    app.jinja_env.auto_reload = False
    app.jinja_env.loader = jinja2.ModuleLoader('templates_compiled.zip')


# Install dpxdt.server override hooks.
from dpxdt.server import api
import hooks

api._artifact_created = hooks._artifact_created
api._get_artifact_response = hooks._get_artifact_response


# Don't log when appstats is active.
appstats_DUMP_LEVEL = -1

# SQLAlchemy stacks are really deep.
appstats_MAX_STACK = 20

# Use very shallow local variable reprs to reduce noise.
appstats_MAX_DEPTH = 2


def gae_mini_profiler_should_profile_production():
    from google.appengine.api import users
    return users.is_current_user_admin()


def gae_mini_profiler_should_profile_development():
    return False


# Fix the appstats module's formatting helper function.
import appstats_monkey_patch
