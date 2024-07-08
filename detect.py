import os
from github import Github
import re

def detect_duplicates():
    token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('REPO_NAME')
    issue_number = int(os.environ.get('ISSUE_NUMBER'))

    if not all([token, repo_name, issue_number]):
        print("Error: Missing required environment variables.")
        return

    g = Github(token)

    try:
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)

        # Extract keywords from the issue title
        keywords = extract_keywords(issue.title)

        # Search for potential duplicates using keywords
        query = f'is:issue repo:{repo_name} ' + ' OR '.join(keywords)
        print(f"Search query: {query}")

        potential_duplicates = g.search_issues(query)
        print(f"Total results found: {potential_duplicates.totalCount}")

        # Filter and score duplicates
        duplicates = []
        for i in potential_duplicates:
            if i.number != issue_number:
                score = calculate_similarity(issue.title, i.title)
                if score > 0.5:  # Adjust this threshold as needed
                    duplicates.append((i, score))

        # Sort duplicates by similarity score and take top 5
        duplicates.sort(key=lambda x: x[1], reverse=True)
        duplicates = duplicates[:5]

        if duplicates:
            comment = "This issue might be a duplicate. Please check these similar issues:\n\n"
            for dup, score in duplicates:
                comment += f"- #{dup.number}: {dup.title} (Similarity: {score:.2f})\n"
            comment += "\nIf this is indeed a duplicate, please close this issue. If not, please provide more details on how this issue differs."
            
            issue.create_comment(comment)
            issue.add_to_labels('potential-duplicate')
            
            print(f"Potential duplicates found for issue #{issue_number}. Comment added and label applied.")
        else:
            print(f"No potential duplicates found for issue #{issue_number}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def extract_keywords(title):
    # Convert to lowercase and remove punctuation
    title = re.sub(r'[^\w\s]', '', title.lower())
    words = title.split()
    # Include individual words and pairs of consecutive words
    keywords = words + [' '.join(words[i:i+2]) for i in range(len(words)-1)]
    return list(set(keywords))  # Remove duplicates

def calculate_similarity(title1, title2):
    words1 = set(extract_keywords(title1))
    words2 = set(extract_keywords(title2))
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union)

detect_duplicates()
