import os
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

WIKI_REPO_URL = "https://github.com/samhuynhle/stitching2d.wiki.git"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_WIKI_DIR = os.path.join(BASE_DIR, "docs", "wiki")
TEMP_WIKI_DIR = os.path.join(BASE_DIR, "build", "wiki_git")


def run_cmd(cmd, cwd=None):
    print(f"⚙️ Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error ({res.returncode}): {res.stderr.strip()}")
        return False, res.stderr
    print(f"✅ Success: {res.stdout.strip()}")
    return True, res.stdout


def sync_wiki():
    if os.path.exists(TEMP_WIKI_DIR):
        shutil.rmtree(TEMP_WIKI_DIR, ignore_errors=True)
    os.makedirs(os.path.dirname(TEMP_WIKI_DIR), exist_ok=True)

    print(f"📦 Cloning GitHub Wiki repo: {WIKI_REPO_URL}")
    success, _ = run_cmd(["git", "clone", WIKI_REPO_URL, TEMP_WIKI_DIR])
    
    if not success:
        print("\n⚠️ NOTICE: The GitHub Wiki repository has not been created yet on GitHub.")
        print("To enable it: Go to https://github.com/samhuynhle/stitching2d/wiki and click 'Create the first page'.")
        print("Then run this script again to sync all 6 wiki pages automatically!\n")
        return

    # Copy docs/wiki/*.md to TEMP_WIKI_DIR
    print(f"📂 Copying wiki files from {DOCS_WIKI_DIR}...")
    for item in os.listdir(DOCS_WIKI_DIR):
        src_file = os.path.join(DOCS_WIKI_DIR, item)
        dst_file = os.path.join(TEMP_WIKI_DIR, item)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)
            print(f"  -> {item}")

    # Commit and Push
    run_cmd(["git", "add", "."], cwd=TEMP_WIKI_DIR)
    run_cmd(["git", "commit", "-m", "docs(wiki): update comprehensive documentation pages"], cwd=TEMP_WIKI_DIR)
    success, _ = run_cmd(["git", "push", "origin", "master"], cwd=TEMP_WIKI_DIR)
    if not success:
        run_cmd(["git", "push", "origin", "main"], cwd=TEMP_WIKI_DIR)

    print("\n🎉 GitHub Wiki successfully synced!\n")


if __name__ == "__main__":
    sync_wiki()
