
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
)

from .. import models


@view_config(
    route_name='matakuliah_list',
    request_method='GET',
    renderer='json'
)
def get_all(request):
    dbsession = request.dbsession
    data = dbsession.query(models.Matakuliah).all()

    return [item.to_dict() for item in data]


@view_config(
    route_name='matakuliah_detail',
    request_method='GET',
    renderer='json'
)
def get_by_id(request):
    dbsession = request.dbsession
    matakuliah_id = int(request.matchdict['id'])

    data = dbsession.query(models.Matakuliah).filter_by(
        id=matakuliah_id
    ).first()

    if data is None:
        raise HTTPNotFound(json_body={
            'error': 'Matakuliah tidak ditemukan'
        })

    return data.to_dict()


@view_config(
    route_name='matakuliah_create',
    request_method='POST',
    renderer='json'
)
def create(request):
    data = request.json_body
    required = ['kode_mk', 'nama_mk', 'sks', 'semester']

    for field in required:
        if field not in data or data[field] in (None, ''):
            raise HTTPBadRequest(json_body={
                'error': f'{field} wajib diisi'
            })

    try:
        sks = int(data['sks'])
        semester = int(data['semester'])
    except (ValueError, TypeError):
        raise HTTPBadRequest(json_body={
            'error': 'SKS dan semester harus berupa angka'
        })

    if sks <= 0 or semester <= 0:
        raise HTTPBadRequest(json_body={
            'error': 'SKS dan semester harus lebih dari 0'
        })

    dbsession = request.dbsession

    existing = dbsession.query(models.Matakuliah).filter_by(
        kode_mk=data['kode_mk']
    ).first()

    if existing:
        raise HTTPBadRequest(json_body={
            'error': 'Kode matakuliah sudah digunakan'
        })

    matakuliah = models.Matakuliah(
        kode_mk=data['kode_mk'],
        nama_mk=data['nama_mk'],
        sks=sks,
        semester=semester
    )

    dbsession.add(matakuliah)
    dbsession.flush()

    return matakuliah.to_dict()


@view_config(
    route_name='matakuliah_update',
    request_method='PUT',
    renderer='json'
)
def update(request):
    matakuliah_id = int(request.matchdict['id'])
    dbsession = request.dbsession

    matakuliah = dbsession.query(models.Matakuliah).filter_by(
        id=matakuliah_id
    ).first()

    if matakuliah is None:
        raise HTTPNotFound(json_body={
            'error': 'Matakuliah tidak ditemukan'
        })

    data = request.json_body
    required = ['kode_mk', 'nama_mk', 'sks', 'semester']

    for field in required:
        if field not in data or data[field] in (None, ''):
            raise HTTPBadRequest(json_body={
                'error': f'{field} wajib diisi'
            })

    try:
        sks = int(data['sks'])
        semester = int(data['semester'])
    except (ValueError, TypeError):
        raise HTTPBadRequest(json_body={
            'error': 'SKS dan semester harus berupa angka'
        })

    if sks <= 0 or semester <= 0:
        raise HTTPBadRequest(json_body={
            'error': 'SKS dan semester harus lebih dari 0'
        })

    existing = dbsession.query(models.Matakuliah).filter(
        models.Matakuliah.kode_mk == data['kode_mk'],
        models.Matakuliah.id != matakuliah_id
    ).first()

    if existing:
        raise HTTPBadRequest(json_body={
            'error': 'Kode matakuliah sudah digunakan'
        })

    matakuliah.kode_mk = data['kode_mk']
    matakuliah.nama_mk = data['nama_mk']
    matakuliah.sks = sks
    matakuliah.semester = semester

    dbsession.flush()

    return matakuliah.to_dict()


@view_config(
    route_name='matakuliah_delete',
    request_method='DELETE',
    renderer='json'
)
def delete(request):
    matakuliah_id = int(request.matchdict['id'])
    dbsession = request.dbsession

    matakuliah = dbsession.query(models.Matakuliah).filter_by(
        id=matakuliah_id
    ).first()

    if matakuliah is None:
        raise HTTPNotFound(json_body={
            'error': 'Matakuliah tidak ditemukan'
        })

    dbsession.delete(matakuliah)

    return {
        'message': 'Matakuliah berhasil dihapus'
    }
