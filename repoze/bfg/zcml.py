from zope.component.zcml import handler
from zope.component.interface import provideInterface
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import Bool

from zope.interface import Interface
from zope.interface import implements

from zope.schema import TextLine

from repoze.bfg.interfaces import IRequest
from repoze.bfg.interfaces import IViewPermission
from repoze.bfg.interfaces import IView
from repoze.bfg.interfaces import ISettings

from repoze.bfg.security import ViewPermissionFactory

def _handler(*arg, **kw):
    import pdb; pdb.set_trace()
    return handler(*arg, **kw)

class Settings(object):
    implements(ISettings)
    def __init__(self, reload_templates=False):
        self.reload_templates = reload_templates

def settings(_context, reload_templates=False):
    settings = Settings(reload_templates=reload_templates)
    _context.action(
        discriminator = ('settings', ISettings),
        callable = handler,
        args = ('registerUtility', settings, ISettings, '', _context.info),
        )

class ISettingsDirective(Interface):
    reload_templates = Bool(
        title=u"Reload templates when they change",
        description=(u"Specifies whether templates should be reloaded when"
                     "a change is made"),
        default=False)

def view(_context,
         permission=None,
         for_=None,
         view=None,
         name="",
         request_type=IRequest,
         ):

    if not view:
        raise ConfigurationError('"view" attribute was not specified')

    if for_ is not None:
        _context.action(
            discriminator = None,
            callable = provideInterface,
            args = ('', for_)
            )

    if permission:
        pfactory = ViewPermissionFactory(permission)
        _context.action(
            discriminator = ('permission', for_,name, request_type,
                             IViewPermission),
            callable = handler,
            args = ('registerAdapter',
                    pfactory, (for_, request_type), IViewPermission, name,
                    _context.info),
            )

    _context.action(
        discriminator = ('view', for_, name, request_type, IView),
        callable = handler,
        args = ('registerAdapter',
                view, (for_, request_type), IView, name,
                _context.info),
        )

class IViewDirective(Interface):
    for_ = GlobalObject(
        title=u"The interface or class this view is for.",
        required=False
        )

    permission = TextLine(
        title=u"Permission",
        description=u"The permission needed to use the view.",
        required=False
        )

    view = GlobalObject(
        title=u"",
        description=u"The view function",
        required=False,
        )

    name = TextLine(
        title=u"The name of the view",
        description=u"""
        The name shows up in URLs/paths. For example 'foo' or
        'foo.html'.""",
        required=False,
        )

    request_type = GlobalObject(
        title=u"""The request type interface for the view""",
        description=(u"The view will be called if the interface represented by "
                     u"'request_type' is implemented by the request.  The "
                     u"default request type is repoze.bfg.interfaces.IRequest"),
        required=False
        )


