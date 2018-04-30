import pytest
from vyper import compiler


def test_compiling():
    pool = open('./pool.v.py').read()
    assert compiler.compile(pool)