from setuptools import setup


setup(
    name='cldfbench_kitchen_et_al2009',
    py_modules=['cldfbench_kitchen_et_al2009'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'kitchen_et_al2009=cldfbench_kitchen_et_al2009:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
