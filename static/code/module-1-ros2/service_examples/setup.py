from setuptools import setup

package_name = 'service_action_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'minimal_service = service_action_demo.minimal_service:main',
            'minimal_client = service_action_demo.minimal_client:main',
            'minimal_action_server = service_action_demo.minimal_action_server:main',
            'minimal_action_client = service_action_demo.minimal_action_client:main',
        ],
    },
)