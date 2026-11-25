
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')

    config.add_route(
        'matakuliah_list',
        '/api/matakuliah',
        request_method='GET'
    )

    config.add_route(
        'matakuliah_create',
        '/api/matakuliah',
        request_method='POST'
    )

    config.add_route(
        'matakuliah_detail',
        r'/api/matakuliah/{id:\d+}',
        request_method='GET'
    )

    config.add_route(
        'matakuliah_update',
        r'/api/matakuliah/{id:\d+}',
        request_method='PUT'
    )

    config.add_route(
        'matakuliah_delete',
        r'/api/matakuliah/{id:\d+}',
        request_method='DELETE'
    )
