import pytest
import s3logparse

LOGFILE = 'tests/test.log'
NAME = 's3logparse.py'

def test_humanreadablesize():
    assert s3logparse.humanreadablesize(10000) == '9.77 KiB'

def test_main_toptalkers(mocker, capsys):
    mocker.patch(
            "sys.argv",
                [
                NAME,
                'toptalkers',
                LOGFILE
                ],
            )
    s3logparse.main()
    captured = capsys.readouterr()
    assert captured.out == '765.00 B - 192.0.2.3\n'

def test_main_useragent(mocker, capsys):
    mocker.patch(
            "sys.argv",
                [
                NAME,
                'useragent',
                LOGFILE
                ],
            )
    s3logparse.main()
    captured = capsys.readouterr()
    assert captured.out == '5 - S3Console/0.4\n'


def test_main_topuploaders(mocker, capsys):
    mocker.patch(
            "sys.argv",
                [
                NAME,
                'topuploaders',
                LOGFILE
                ],
            )
    s3logparse.main()
    captured = capsys.readouterr()
    assert captured.out == ''


def test_main_topdownloaders(mocker, capsys):
    mocker.patch(
            "sys.argv",
                [
                NAME,
                'topdownloaders',
                LOGFILE
                ],
            )
    s3logparse.main()
    captured = capsys.readouterr()
    assert captured.out == '765.00 B - 192.0.2.3\n'


def test_main_topfiles(mocker, capsys):
    mocker.patch(
            "sys.argv",
                [
                NAME,
                'topfiles',
                LOGFILE
                ],
            )
    s3logparse.main()
    captured = capsys.readouterr()
    assert captured.out == '1 - s3-dg.pdf\n'

