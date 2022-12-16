import os, json, shutil, sys
from pathlib import Path

BASE_PATH = Path(os.path.realpath(__file__)).parent.parent
BUILD_PATH = Path(os.path.join(BASE_PATH, 'dist'))
SRC_PATH = Path(os.path.join(BASE_PATH, 'src'))

MANIFEST_NAME = 'master-manifest.json'

ENV_DOMAIN_PLACEHOLDER = '{CDN_BASE_URL}'
ENV_DOMAIN_VALUE = os.getenv('DEPLOY_DIRECTORY') #does not raise an exception, but returns None

def main():
    build_exists = os.path.exists(BUILD_PATH)
    if build_exists:
        shutil.rmtree(BUILD_PATH) # remove the build path (dist/) directory tree
    shutil.copytree(SRC_PATH, BUILD_PATH, ignore=shutil.ignore_patterns('manifest.json')) # copy from src/ to dist/

    manifest_json = { "model_manifests" : [] } # create dict with key of 'model_manifests'
    manifests = sorted(SRC_PATH.rglob('*manifest.json')) # create list sorted on SRC_PATH with *manifest.json
    for manifest_path in manifests:
        with open(manifest_path, 'r') as file:
            mini_manifest = json.load(file)
        # replace variables:
        base_url = str(mini_manifest['files']['baseUrl'])
        if ENV_DOMAIN_VALUE is None:
            sys.exit("ENV_DOMAIN is not set")
        mini_manifest['files']['baseUrl'] = base_url.replace(ENV_DOMAIN_PLACEHOLDER, ENV_DOMAIN_VALUE)
        manifest_json["model_manifests"].append(mini_manifest)

    master_manifest = os.path.join(BUILD_PATH, MANIFEST_NAME)
    with open(master_manifest, 'w') as file:
        # compressing the json result saves ~42% on size
        json.dump(manifest_json, file, ensure_ascii=False, separators=(',', ':'))

if __name__ == '__main__':
    main()
