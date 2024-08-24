import os
import requests
from difflib import SequenceMatcher

def run_query(query, variables):
    headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers, timeout=60)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed with status code: {request.status_code}. {request.json()}")

def calculate_similarity(title1, title2):
    return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

def detect_duplicates():
    repo_owner, repo_name = os.environ['REPO_NAME'].split('/')
    issue_number = int(os.environ['ISSUE_NUMBER'])

    # GraphQL query to get the issue title and search for similar issues
    query = """
    query($owner: String!, $name: String!, $number: Int!) {
      repository(owner: $owner, name: $name) {
        issue(number: $number) {
          title
        }
        issues(first: 100, states: OPEN) {
          nodes {
            number
            title
          }
        }
      }
    }
    """

    variables = {
        "owner": repo_owner,
        "name": repo_name,
        "number": issue_number
    }

    result = run_query(query, variables)
    
    if result.get("errors"):
        print(f"GraphQL query failed: {result['errors']}")
        return

    data = result["data"]["repository"]
    current_issue_title = data["issue"]["title"]
    all_issues = data["issues"]["nodes"]

    duplicates = []
    for issue in all_issues:
        if issue["number"] != issue_number:
            score = calculate_similarity(current_issue_title, issue["title"])
            if score > 0.5:  # Adjust this threshold as needed
                duplicates.append((issue, score))

    duplicates.sort(key=lambda x: x[1], reverse=True)
    duplicates = duplicates[:5]

    if duplicates:
        comment = "This issue might be a duplicate. Please check these similar issues:\n\n"
        for dup, score in duplicates:
            comment += f"- #{dup['number']}: {dup['title']} (Similarity: {score:.2f})\n"
        comment += "\nIf this is indeed a duplicate, please close this issue. If not, please provide more details on how this issue differs."
        
        # Add comment to the issue (using REST API as it's simpler for this operation)
        add_comment_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
        headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
        response = requests.post(add_comment_url, json={"body": comment}, headers=headers)
        
        if response.status_code == 201:
            print(f"Potential duplicates found for issue #{issue_number}. Comment added.")
        else:
            print(f"Failed to add comment. Status code: {response.status_code}")
        
        # Add label to the issue
        add_label_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/labels"
        response = requests.post(add_label_url, json={"labels": ["potential-duplicate"]}, headers=headers)
        
        if response.status_code == 200:
            print("Label 'potential-duplicate' applied.")
        else:
            print(f"Failed to add label. Status code: {response.status_code}")
    else:
        print(f"No potential duplicates found for issue #{issue_number}.")

if __name__ == "__main__":
    detect_duplicates()
