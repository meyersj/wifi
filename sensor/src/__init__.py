"""
try to create newrelic application if the agent is installed
"""
application = None
agent = None
try:
    import newrelic.agent as agent
    application = agent.application()
except:
    pass
