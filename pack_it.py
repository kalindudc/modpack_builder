#!/usr/bin/env python3

import os
from string import Template
import zipfile

# change these variables to match your modpack
MODPACK_NAME = "BIG Modpack"
MODPACK_VERSION = "0.1.5"

BUILD_DIR = "./build"
THINGS_TO_CHANGE_PATH = "./THINGS_TO_CHANGE"
SETUP_TEMPLATE_PATH = "./setup.bat.template"

MODPACK_DIR = "./modpack/"
MODPACK_SERVER_DIR = "./modpack_server/"
MODPACK_PROFILE_VERSION_DIR = "./modpack_profile_version/"
MODPACK_BUILDER_VERSIONS_DIR = "./builder_versions/"

MODPACK_VERSION_FILE_RELATIVE_PATH = "config/bcc-common.toml"
BCC_COMMON_FILE_CONTENTS = f'''
[general]
	modpackProjectID = 0
	modpackName = "{MODPACK_NAME}"
	modpackVersion = "{MODPACK_VERSION}"
	useMetadata = false
'''

def main():
  with open(THINGS_TO_CHANGE_PATH, "r") as things_to_change_file:
    lines = things_to_change_file.readlines()
    print("Things to change: ")
    for line in lines:
      print(f"\t{line.strip()}")

  confirmation = input("Are you sure you want to continue? (y/n): ")
  if confirmation.lower() != "y":
    print("Exiting...")
    return

  print("\n")
  update_modpack_version()
  pack_modpack()
  pack_server()
  pack_profile_version()
  generate_setup_file()
  create_new_builder_version()

def create_new_builder_version():
  print ("Creating new builder version...")
  zip_name = f"big_modpack_builder_{MODPACK_VERSION}.zip"
  pack(BUILD_DIR, zip_name, MODPACK_BUILDER_VERSIONS_DIR)

def update_modpack_version():
  print("Updating modpack version for modpack and server...")
  modpack_bcc_common_path = os.path.join(MODPACK_DIR, MODPACK_VERSION_FILE_RELATIVE_PATH)
  modpack_server_bcc_common_path = os.path.join(MODPACK_SERVER_DIR, MODPACK_VERSION_FILE_RELATIVE_PATH)

  with open(modpack_bcc_common_path, "w") as modpack_bcc_common_file:
    modpack_bcc_common_file.write(BCC_COMMON_FILE_CONTENTS)

  with open(modpack_server_bcc_common_path, "w") as modpack_server_bcc_common_file:
    modpack_server_bcc_common_file.write(BCC_COMMON_FILE_CONTENTS)

  print(f"\tUpdated modpack version to {MODPACK_VERSION} in {modpack_bcc_common_path} and {modpack_server_bcc_common_path}")

def pack_modpack():
  print("Packing modpack...")
  pack(MODPACK_DIR, zip_name="modpack.zip")

def pack_server():
  print("Packing modpack server...")
  pack(MODPACK_SERVER_DIR, zip_name="modpack_server.zip")

def pack_profile_version():
  print("Packing profile version...")
  pack(MODPACK_PROFILE_VERSION_DIR, zip_name="profile_version.zip")

def pack(contents_dir, zip_name=None, build_dir=BUILD_DIR):
  # using the contents of MODPACK_DIR, create .zip in BUILD_DIR
  if zip_name is None:
    zip_name = os.path.dirname(contents_dir) + ".zip"
  zip_path = os.path.join(build_dir, zip_name)

  with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(contents_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, contents_dir)
            zipf.write(full_path, arcname)

  print(f'\t{zip_name} created successfully in {build_dir}')

def generate_setup_file():
  print("Generating setup file...")
  profile_version_id = get_profile_version_id()

  # read the template file
  setup_template_contents = ""
  with open(SETUP_TEMPLATE_PATH, "r") as setup_template_file:
    setup_template_contents = setup_template_file.read()

  variables = {
    "modpack_name": MODPACK_NAME.replace(" ", ""),
    "modpack_version": MODPACK_VERSION,
    "profile_version_id": profile_version_id
  }
  template = Template(setup_template_contents)
  setup_contents = template.safe_substitute(variables)

  # write the setup file
  with open(BUILD_DIR + "/setup.bat", "w") as setup_file:
    setup_file.write(setup_contents)

  print(f"\tSetup file written to {BUILD_DIR}/setup.bat, for modpack {MODPACK_NAME} version {MODPACK_VERSION} with Profile version {profile_version_id}")


def get_profile_version_id():
  files = os.listdir(MODPACK_PROFILE_VERSION_DIR)
  if len(files) == 0:
    raise Exception("No Profile version found")

  for file in files:
    if file.endswith(".jar"):
      return file.strip(".jar")

  raise Exception("No Profile version found")


if __name__ == "__main__":
  main()
