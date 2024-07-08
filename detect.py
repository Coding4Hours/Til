import os
from github import Github

def detect_duplicates():
    # Authentication for user filing issue (must have read/write access to repository to add labels)
    token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('REPO_NAME')
    issue_number = int(os.environ.get('ISSUE_NUMBER'))

    if not all([token, repo_name, issue_number]):
        print("Error: Missing required environment variables.")
        return

    # Create a Github instance
    g = Github(token)

    try:
        # Get the repository
        repo = g.get_repo(repo_name)

        # Get the issue
        issue = repo.get_issue(number=issue_number)

        # Search for potential duplicates
        query = f'is:issue repo:{repo_name} {issue.title}'
        potential_duplicates = g.search_issues(query)

        # Filter out the current issue and limit to top 5 results
        duplicates = [i for i in potential_duplicates if i.number != issue_number][:5]

        if duplicates:
            # Create a comment with links to potential duplicates
            comment = "This issue might be a duplicate. Please check these similar issues:\n\n"
            for dup in duplicates:
                comment += f"- #{dup.number}: {dup.title}\n"
            comment += "\nIf this is indeed a duplicate, please close this issue. If not, please provide more details on how this issue differs."
            
            # Add the comment to the issue
            issue.create_comment(comment)
            
            # Add a 'potential-duplicate' label
            issue.add_to_labels('potential-duplicate')
            
            print(f"Potential duplicates found for issue #{issue_number}. Comment added and label applied.")
        else:
            print(f"No potential duplicates found for issue #{issue_number}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    detect_duplicates()
