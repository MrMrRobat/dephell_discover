from collections import defaultdict

import pytest

from dephell_discover import Root


def test_discover_packages(tmp_path):
    p = Root(path=tmp_path)
    path = tmp_path / 'project1'

    path.mkdir()
    (path / 'dir1').mkdir()
    (path / 'dir2').mkdir()
    (path / 'dir3').mkdir()
    (path / 'dir3' / 'dir4').mkdir()
    (path / 'empty').mkdir()
    (path / '__pycache__').mkdir()

    (tmp_path / 'ignore.json').touch()
    (path / '__init__.py').touch()
    (path / 'file1.py').touch()
    (path / 'file2.db').touch()
    (path / 'dir1' / '__init__.py').touch()
    (path / 'dir2' / 'file3.json').touch()

    (path / 'dir3' / '__init__.py').touch()
    (path / 'dir3' / 'dir4' / 'file4.json').touch()

    (path / '__pycache__' / 'lol.pyc').touch()

    assert set(map(str, p.packages)) == {'project1', 'project1.dir1', 'project1.dir3'}

    data = defaultdict(set)
    for f in p.data:
        data[f.module].add(str(f))
    assert set(data) == {'project1', 'project1.dir3'}
    assert data['project1'] == {'*.db', 'dir2/*.json'}
    assert data['project1.dir3'] == {'dir4/*.json'}


@pytest.mark.parametrize('name, files, expected', [
    ['foobar', ('foobar/__init__.py', 'foobar/foo.py', 'foobar/bar.py'), {'': ''}],
    ['foobar', ('src/__init__.py', 'src/foo.py', 'src/bar.py'), {'foobar': 'src'}],
    ['foobar', ('__init__.py', 'foo.py', 'bar.py'), {'foobar': ''}],
    ['foobar', ('src/foobar/__init__.py', 'src/foobar/foo.py', 'src/foobar/bar.py'), {'': 'src'}],
])
def test_package_dir(name, files, expected, tmp_path):
    for file_path in files:
        path = tmp_path.joinpath(file_path)
        if '/' in file_path:
            path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    root = Root(path=tmp_path, name=name)
    assert root.package_dir == expected
