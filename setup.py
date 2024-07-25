from setuptools import setup, find_packages

setup(
    name='ann_ai_internal_poc',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'google-cloud-storage',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'embedding=commands.embedding:main',
        ],
    },
)