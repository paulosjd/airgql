def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('index', '/index')
    config.add_route('sites', '/sites')
    config.add_route('site_aq_data', '/data/{site_id}')
    config.add_route('graphiql', '/graphiql')
