from setuptools import setup

package_name = 'line_follow'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ju Young',
    maintainer_email='ju@kookmin.ac.kr',
    description='Color line follower',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'color_line_follower_node = line_follow.line_follow:main',
        ],
    },
)

