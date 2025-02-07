from setuptools import find_packages, setup
import os 
from glob import glob

package_name = 'rover_gazebosim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.py*'))),
        (os.path.join('share',package_name,'urdf','urdf'),glob('urdf/urdf/*.urdf')),
        (os.path.join('share',package_name,'urdf','urdf'),glob('urdf/urdf/rover.gazebo')),
        (os.path.join('share',package_name,'meshes'),glob('urdf/meshes/*.STL')),
        (os.path.join('share',package_name,'urdf'),glob('urdf/*.xacro')),
        (os.path.join('share',package_name,'config'),glob('config/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dhher',
    maintainer_email='dheer968793@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
