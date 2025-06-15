import sys
import json
from github import Github

comments_file = sys.argv[1]
pr_number = int(sys.argv[2])

with open(comments_file) as f:
    comments = json.load(f)["comments"]

g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo("Bryan-Roe-ai/semantic-kernel")
pr = repo.get_pull(pr_number)

for c in comments:
    pr.create_review_comment(
        body=c["comment"],
        commit_id=pr.head.sha,
        path=c["file"],
        line=c["line"]
    )
