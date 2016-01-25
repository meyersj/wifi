import os


ENV = "NEW_RELIC_CONFIG_FILE"

"""
these two objects will be imported from PostHandler,
if they are empty new relic monitoring will not happen
"""
application = None
agent = None

filepath = os.path.dirname(os.path.realpath(__file__))
default_config = os.path.join(os.path.dirname(filepath), "newrelic/newrelic.ini")
monitor = False
config = os.environ.get(ENV, "")
if config and os.path.isfile(config):
    monitor = True
else:
    config = default_config
    if os.path.isfile(config):
        monitor = True
        os.environ[ENV] = config
if monitor:
    print "MONITORING"
    import newrelic.agent as agent
    application = agent.application()
