from pkg_resources import working_set
from . import EXTRACTORS
from . import Message
from . import check_c_format
from . import check_python_format
from . import Extractor


DEFAULT_KEYWORDS = {
        '_': None,
        'gettext': None,
        'ngettext': (1, 2),
        'ugettext': None,
        'ungettext': (1, 2),
        'dgettext': (2,),
        'dngettext': (2, 3),
        'N_': None,
        'pgettext': ((1, 'c'), 2)
        }


class BabelExtractor(Extractor):
    extensions = []
    extractor = None

    def __call__(self, filename, options):
        fileobj = open(filename, 'rb')
        for (lineno, _, msgid, comment) in self.extractor(fileobj, DEFAULT_KEYWORDS.keys(), (), {}):
            flags = []
            check_c_format(msgid, flags)
            check_python_format(msgid, flags)
            yield Message(None, msgid, u'', flags, comment, None, (filename, lineno))


def register_babel_plugins():
    for entry_point in working_set.iter_entry_points('babel.extractors'):
        name = entry_point.name
        extractor = entry_point.load(require=True)
        cls = type('BabelExtractor_%s' % name,
                (BabelExtractor, object),
                {'extractor': extractor,
                 '__doc__': extractor.__doc__})
        EXTRACTORS['babel-%s' % name] = cls()
