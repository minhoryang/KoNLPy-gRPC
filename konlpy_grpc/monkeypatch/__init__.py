""".

# follow gevent monkeypatch library way.

# Usage:
>>> import konlpy_grpc
>>> konlpy_grpc.patch()
>>> konlpy_grpc.configure(server='[::]:50051')
>>> import konlpy
>>> konlpy.tag.Hannanum().pos('안녕 세상아!')  # Same As Usual...
"""

import types


_ORIGINAL = {}  # TODO: contextvar?
KEY_INIT_JVM = "konlpy.jvm.init_jvm"
KEY_TAG_HANNANUM = "konlpy.tag._hannanum.Hannanum"
KEY_TAG_KKMA = "konlpy.tag._kkma.Kkma"
KEY_TAG_KOMORAN = "konlpy.tag._komoran.Komoran"
KEY_TAG_MECAB = "konlpy.tag._mecab.Mecab"
KEY_TAG_OKT = "konlpy.tag._okt.Okt"
PATCH_KEYS = (KEY_INIT_JVM, KEY_TAG_HANNANUM, KEY_TAG_KKMA, KEY_TAG_KOMORAN, KEY_TAG_MECAB, KEY_TAG_OKT)


def isPatched():
    # FIXME: check after fork() or whatever.
    # Is it really enough? I don't think so. (use sys.modules? importlib?)
    for key in PATCH_KEYS:
        if key not in _ORIGINAL:
            return False
    return True


def patch(without_jpype=False):
    import konlpy

    if isPatched():
        return

    if not without_jpype:
        _ORIGINAL[KEY_INIT_JVM] = konlpy.jvm.init_jvm
        # XXX: also cover up jpype.isJVMStarted().
    else:
        _ORIGINAL[KEY_INIT_JVM] = None

    _ORIGINAL[KEY_TAG_HANNANUM] = konlpy.tag._hannanum.Hannanum
    _ORIGINAL[KEY_TAG_KKMA] = konlpy.tag._kkma.Kkma
    _ORIGINAL[KEY_TAG_KOMORAN] = konlpy.tag._komoran.Komoran
    _ORIGINAL[KEY_TAG_MECAB] = konlpy.tag._mecab.Mecab
    _ORIGINAL[KEY_TAG_OKT] = konlpy.tag._okt.Okt

    if not without_jpype:
        konlpy.init_jvm = konlpy.jvm.init_jvm = lambda *args, **kwargs: None  # insert warning here?

    from ..clients.hannanum_client import HannanumClient
    from ..clients.kkma_client import KkmaClient
    from ..clients.komoran_client import KomoranClient
    from ..clients.mecab_client import MecabClient
    from ..clients.okt_client import OktClient

    konlpy.tag.Hannanum = konlpy.tag._hannanum.Hannanum = shim_class("Hannanum", konlpy.tag._hannanum.Hannanum, HannanumClient)
    konlpy.tag.Kkma = konlpy.tag._kkma.Kkma = shim_class("Kkma", konlpy.tag._kkma.Kkma, KkmaClient)
    konlpy.tag.Komoran = konlpy.tag._komoran.Komoran = shim_class("Kkma", konlpy.tag._komoran.Komoran, KomoranClient)
    konlpy.tag.Mecab = konlpy.tag._mecab.Mecab = shim_class("Kkma", konlpy.tag._mecab.Mecab, MecabClient)
    konlpy.tag.Okt = konlpy.tag._okt.Okt = shim_class("Kkma", konlpy.tag._okt.Okt, OktClient)
    # XXX: Respect the konlpy.tag._okt.Twitter()'s warning and It gonna be deprecated soon.


def revert(fatal=False):
    import konlpy

    if not isPatched():
        if fatal:
            raise Exception()  # FIXME
        return

    with_jpype = _ORIGINAL.pop(KEY_INIT_JVM, False)
    if with_jpype:
        konlpy.init_jvm = konlpy.jvm.init_jvm = with_jpype

    konlpy.tag.Hannanum = konlpy.tag._hannanum.Hannanum = _ORIGINAL.pop(KEY_TAG_HANNANUM)
    konlpy.tag.Kkma = konlpy.tag._kkma.Kkma = _ORIGINAL.pop(KEY_TAG_KKMA)
    konlpy.tag.Komoran = konlpy.tag._komoran.Komoran = _ORIGINAL.pop(KEY_TAG_KOMORAN)
    konlpy.tag.Mecab = konlpy.tag._mecab.Mecab = _ORIGINAL.pop(KEY_TAG_MECAB)
    konlpy.tag.Okt = konlpy.tag._okt.Okt = _ORIGINAL.pop(KEY_TAG_OKT)


def shim_class(name, konlpy__clz, konlpy_grpc__clz):
    shim = type(name, (Patched, konlpy_grpc__clz), {})
    # name, bases, dict

    shim.__doc__ = konlpy_grpc__clz.__doc__
    if konlpy__clz.__doc__ and not shim.__doc__:
        shim.__doc__ = konlpy__clz.__doc__

    for key, value in konlpy__clz.__dict__.items():
        shim_key = getattr(shim, key, None)
        if isinstance(value, types.FunctionType) and value.__doc__ and shim_key and not shim_key.__doc__:
            shim_key.__doc__ = value.__doc__
    return shim


class Patched:
    def __init__(self, jvmpath=None, max_heap_size=1024, *args, **kwargs):
        # TODO: insert Warning here!
        super().__init__(*args, **kwargs)
