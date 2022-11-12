import pytest

def compare_versions(version1, version2):

    versions1 = [int(i) for i in version1.split('.')]
    versions2 = [int(i) for i in version2.split('.')]

    print(versions1)
    print(versions2)
    print('-------------------')
    for idx, version in enumerate(versions1):
        #print(f"version {version}")
        print(f"version2 {versions2[idx]}")
        if version > versions2[idx]:
            return 1
        elif version < versions2[idx]:
            return -1
        print(" ")
    return 0

def test_compare_versions():
    version = [int(i) for i in '7.2.7.1'.split('.')]
    limit_version = [7,2,7]

    assert limit_version < version

    version = [int(i) for i in '7.2.7.1'.split('.')]
    limit_version = [7,2,7,1]

    assert limit_version == version

def test_string_format():
    print("Exception %s", None)
