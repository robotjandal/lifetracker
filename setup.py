import io

from setuptools import find_packages, setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()


setup(
    name="lifetracker",
    version="0.0.1dev",
    # maintainer='',
    # maintainer_email='',
    # license='',
    description="Tracking aspects of oneself (e.g. goals, vices).",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extra_require={"test": ["pytest", "coverage"]},
)
