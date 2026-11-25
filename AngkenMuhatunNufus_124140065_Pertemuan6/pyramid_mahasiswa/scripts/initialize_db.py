
import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    matakuliah = [
        models.Matakuliah(
            kode_mk='IF101',
            nama_mk='Algoritma dan Pemrograman',
            sks=3,
            semester=1
        ),
        models.Matakuliah(
            kode_mk='IF202',
            nama_mk='Struktur Data',
            sks=3,
            semester=2
        ),
        models.Matakuliah(
            kode_mk='IF303',
            nama_mk='Basis Data',
            sks=3,
            semester=3
        )
    ]

    dbsession.add_all(matakuliah)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.
Check your database connection and Alembic migration.
        ''')
