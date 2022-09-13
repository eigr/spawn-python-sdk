"""
Copyright 2022 Eigr.
Licensed under the Apache License, Version 2.0.
"""
import os
import pathlib

from setuptools import find_packages, setup

# Load version in cloudstate package.
from setuptools.command.build_py import build_py

exec(open("spawn/version.py").read())

PROTOBUF_VERSION = "master"

version = __version__  # noqa
name = "spawn"

print(f"package name: {name}, version: {version}", flush=True)

proto_lib_roots = ["protobuf"]
proto_roots = ["."]


class FetchBuildProtosCommand(build_py):
    """fetch libs and install the protocol buffer generated sources."""

    def run(self):
        os.system(f"scripts/fetch-spawn-pb.sh {PROTOBUF_VERSION}")

        for proto_root in proto_roots + proto_lib_roots:
            for root, subdirs, files in os.walk(proto_root):
                for file in [f for f in files if f.endswith(".proto")]:
                    file_path = pathlib.Path(root) / file
                    destination = "."
                    print(f"compiling {file_path} to {destination}")
                    command = f"python -m grpc_tools.protoc {' '.join([' -I ' + i for i in proto_roots + proto_lib_roots])} --python_out={destination} --grpc_python_out={destination} {file_path}"  # noqa
                    os.system(command)

        return super().run()


packages = find_packages(exclude=[])

print(f"packages: {packages}")
setup(
    name=name,
    version=version,
    url="https://github.com/eigr-labs/spawn-python-sdk",
    license="Apache 2.0",
    description="Spawn Python SDK",
    packages=packages,
    package_data={
        "": ["*.proto"],
    },
    long_description=open("Description.md", "r").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    scripts=["scripts/fetch-spawn-pb.sh"],
    install_requires=[
        "attrs>=21.4.0",
        "google-api>=0.1.12",
        "googleapis-common-protos>=1.56.4",
        "grpcio>=1.48.1",
        "grpcio-tools>=1.0.0",
        "flask>=2.1.3",
        "protobuf>=3.20.0",
        "pytest>=7.1.2",
        "docker",
    ],
    cmdclass={
        "build_py": FetchBuildProtosCommand,
    },
)
