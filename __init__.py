#!/usr/bin/env python

"""
CouchDB
"""

import time
import os

## Needs to be in import path
import settings

from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.http import ResourceNotFound
from couchdb.mapping import ViewField

# pylint: disable=W0403
import list_splitter
# pylint: enable=W0403


try:
    if SERVER:
        pass
except NameError:
    serv_host = getattr(settings, 'COUCHDB_HOST', '127.0.0.1')
    serv_port = getattr(settings, 'COUCHDB_PORT', 5984)
    serv_user = getattr(settings, 'COUCHDB_USER', None)
    serv_pass = getattr(settings, 'COUCHDB_PASS', None)
    if (serv_user is not None) and (serv_pass is not None):
        serv = 'http://%s:%s@%s:%d' % \
            (serv_user, serv_pass, serv_host, serv_port)
    else:
        serv = 'http://%s:%d' % (serv_host, serv_port)
    SERVER = Server(serv)


_dr = os.path.dirname(__file__)
_dr += '/'
_dr += 'design_docs'


def create_db(name):
    """
    If db does not exist, create it

    @author BrendonCrawford
    @param name String
    """
    try:
        if SERVER[name]:
            pass
        print "DB <%s> already exists" % name
    except ResourceNotFound:
        SERVER.create(name)
        print "Created DB <%s>" % name
        return True


def results(db_name, design_doc_name, view_name, **options):
    """
    Grabs raw results without processing

    @author BrendonCrawford
    @param db_name String
    @param design_doc_name String
    @param view_name String
    @options Dict
    """
    res = \
        SERVER[db_name]\
        .view('/'.join((design_doc_name, view_name)), None, **options)
    return res


def list_results(db_name, design_doc_name, view_name, **options):
    """
    Grabs view results in a list

    @author BrendonCrawford
    @param view_name String
    @param options Dict
    @return List
    """
    res = results(db_name, design_doc_name, view_name, **options)
    out = [row.value for row in res.rows]
    return out


def clean_results(res):
    """
    Cleans up results from python-couchdb query

    @author BrendonCrawford
    @param fun Function
    @param db_name String
    @param options Dict
    """
    return map((lambda row: row.value), res.rows)


def upload_views(db_name, map_funcs):
    """
    Wrapper to syncronize a view

    @author BrendonCrawford
    """
    ViewDefinition.sync_many(SERVER[db_name], map_funcs, True)
    print "Uploaded views: <%s>" % db_name
    return True


def all_docs(db_name):
    """
    Gets all docs for a database

    @author BrendonCrawford
    @param db_name String
    @return List
    """
    docs = SERVER[db_name].view('_all_docs', include_docs=True)
    return docs


def empty_db(db_name):
    """
    Empties a db

    @author BrendonCrawford
    @param db_name
    @return Bool
    """
    docs = []
    for x in all_docs(db_name).rows:
        if x.id[0] != '_':
            r = x.value
            r['_id'] = x.id
            r['_rev'] = r['rev']
            r['_deleted'] = True
            del r['rev']
            docs.append(r)
    SERVER[db_name].update(docs)
    return True


def delete_dbs():
    """
    Delete non-system DBS

    @author BrendonCrawford
    """
    dbs = all_dbs()
    for db in dbs:
        if db[0] != '_':
            SERVER.delete(db)
            print "Deleted DB <%s>" % db
    return True


def all_dbs():
    """
    Get listing of all databases

    @author BrendonCrawford
    @return Dict
    """
    path = '_all_dbs'
    _, _, data = _server_get(path)
    return data


def _server_get(path):
    """
    Wrapper for making miscellaneous requests to the server

    @author BrendonCrawford
    @param path String
    """
    status, headers, data = SERVER.resource.get_json(path=path)
    return (status, headers, data)


def update_bulk(dbname, docs, size=200, async=False, delay=0, opts=None):
    """
    Do a server bulk write in chunks
    """
    if len(docs) > 0:
        if opts is None:
            opts = {}
        if async:
            opts['batch'] = 'ok'
        for chunk in list_splitter.chunks_of_n(docs, size):
            SERVER[dbname].update(chunk, **opts)
            if delay > 0:
                time.sleep(delay)
    return True
