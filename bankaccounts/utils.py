from threading import local

sigehos_common_current = local()
sigehos_common_current.audit_user = None


def set_audit_user(usuario):
    sigehos_common_current.audit_user = usuario


def get_audit_user():
    return sigehos_common_current.audit_user
