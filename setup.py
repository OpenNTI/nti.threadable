import codecs
from setuptools import setup, find_packages

entry_points = {
}

TESTS_REQUIRE = [
    'fudge',
    'nose2[coverage_plugin]',
    'nti.testing',
    'pyhamcrest',
    'z3c.baseregistry',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()

setup(
    name='nti.threadable',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Threadable",
    long_description=_read('README.rst'),
    license='Apache',
    keywords='threadable',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'nti.containers',
        'nti.externalization',
        'nti.schema',
        'nti.wref',
        'persistent',
        'zope.component',
        'zope.intid',
        'zope.interface',
        'zope.security'
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    entry_points=entry_points,
)
