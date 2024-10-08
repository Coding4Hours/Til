from datetime import timezone
import git
import pathlib
import sqlite_utils
import urllib.parse

root = pathlib.Path(__file__).parent.resolve()

def created_changed_times(repo_path, ref="master"):
    created_changed_times = {}
    repo = git.Repo(repo_path, odbt=git.GitDB)
    commits = reversed(list(repo.iter_commits(ref)))
    for commit in commits:
        dt = commit.committed_datetime
        affected_files = list(commit.stats.files.keys())
        for filepath in affected_files:
            if filepath not in created_changed_times:
                created_changed_times[filepath] = {
                    "created": dt.isoformat(),
                    "created_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            created_changed_times[filepath].update(
                {
                    "updated": dt.isoformat(),
                    "updated_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            )
    return created_changed_times

def build_database(repo_path):
    all_times = created_changed_times(repo_path)
    db = sqlite_utils.Database(repo_path / "til.db")
    table = db.table("til", pk="path")
    for filepath in root.glob("*/*.md"):
        with filepath.open() as fp:
            # Read all lines of the file
            lines = fp.readlines()
            # Get the fifth line as the title
            if len(lines) >= 5:
                title = lines[4].lstrip("#").strip()
            else:
                title = ""
            # Read the rest of the file as the body
            body = "".join(lines[5:]).strip()
        path = str(filepath.relative_to(root))
        url = f"https://coding4hours.github.io/Til/" + path.replace(" ", "-").replace(".md", "")
        record = {
            "path": path.replace("/", "_"),
            "topic": path.split("/")[0],
            "title": title,
            "url": url,
            "body": body,
        }
        record.update(all_times[path])
        table.insert(record, replace=True)
    if "til_fts" not in db.table_names():
        table.enable_fts(["title", "body"])

if __name__ == "__main__":
    build_database(root)
