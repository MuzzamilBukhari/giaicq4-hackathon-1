from setuptools import find_packages, setup

package_name = 'pub_sub_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='user@example.com',
    description='A minimal publisher/subscriber demo package',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker_node = pub_sub_demo.talker_node:main',
            'listener_node = pub_sub_demo.listener_node:main',
        ],
    },
)
