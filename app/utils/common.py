from flask import abort

response = lambda result: { 'result': result }

def rewrite_abort(code, error):
    abort(code, { 'message': str(error) })
