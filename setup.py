import setuptools
from os import path

README_FP = path.join(path.abspath(path.dirname(__file__)), 'README.md')



setuptools.setup(
    name='thai_tokenizer',
    version='0.2.4',
    description='Fast and accurate Thai tokenization library.',
    long_description=open(README_FP, 'rt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/IDDT/thai-tokenizer',
    author='Kirill Orlov',
    author_email='IDDT@users.noreply.github.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Thai',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords=['thai', 'tokenizer'],
    packages=setuptools.find_packages(exclude=['tests']),
    python_requires='>=3.6',
    include_package_data=True,
    package_data={'': ['data/bpe_merges.jsonl']},
    test_suite='tests',
    zip_safe=True
)
