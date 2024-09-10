# MODPACK BUILDER

This repository contains scripts and template required to building and versioning your modpacks.

### How to use this repo?

```
1. Clone this repo
2. Add modpack files to `./modpack/`
3. Add server files to `./modpack_server/`
4. Add profile verison jars to `./modpack_profile_version/`
    - ./modpack_profile_version
      ├── neoforge-21.1.47.jar
      └── neoforge-21.1.47.json
5. Update MODPACK_NAME and MODPACK_VERSION in pack_it.py
6. Run pack_it.py
```

Above steps will create all necessary archives in `build/` and will create a new builder version in `./builder_versions/`

```
./build
├── modpack.zip
├── modpack_server.zip
├── profile_version.zip
└── setup.bat

./builder_versions
├── modpack_builder_0.1.0.zip
├── ...
└── modpack_builder_1.2.0.zip
```

Run `./build/setup.bat` to create a new modpack instance and a launcher profile for the new version.

### LICENSE
[MIT](./LICENSE)
