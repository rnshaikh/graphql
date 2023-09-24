

def check_permission(permission, context):
    """
    Helper function to resolve permissions.
    Permission can be a string "app_name.perm_codename"
    or callable (lambda) function with user passed as an argument:
    example: lambda(user): user.username.startswith('a')
    """

    if callable(permission):
        if not permission(context.user):
            return False
    else:
        if not context.user.has_perm(permission):
            return False
    return True


def permission_required(permission):

    def function(func):
        def inner(cls, info, *args, **kwargs):
            import pdb
            pdb.set_trace()
            if check_permission(permission, info.context):
                return func(cls, info, *args, **kwargs)
            raise Exception("Permission Denied")
        return inner
    return function



