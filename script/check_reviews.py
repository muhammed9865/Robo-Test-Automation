import requests
import sys
import os

github_token = sys.argv[1]
pr_repo = sys.argv[2]
pr_number = sys.argv[3]
repo_owner = "muhammed9865"

headers = {
    "Authorization": f"Bearer {github_token}",
    'X-GitHub-Api-Version': '2022-11-28'
}

def print_review_status(approved):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        if approved:
            print("review_approved=true", file=fh)
        else:
            print("review_approved=false", file=fh)


def get_reviews():
    url = f"https://api.github.com/repos/{repo_owner}/{pr_repo}/pulls/{pr_number}/reviews"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error getting reviews: {response.text}")
        exit(1)
    else:
        return response.json()

def get_pending_reviews_count() -> int:
    url = f"https://api.github.com/repos/{repo_owner}/{pr_repo}/pulls/{pr_number}/requested_reviewers"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error getting pending reviews: {response.text}")
        exit(1)
    else:
        reviewers = response.json()
        return len(reviewers["users"])
    

def has_all_reviewers_approved(reviews) -> bool:
    approved = False
    pending_reviews = get_pending_reviews_count()
    print(f"Pending reviews: {pending_reviews}")
    if pending_reviews > 0:
        return False
    
    if len(reviews) == 0:
        return False
    
    for review in reviews:
        if review["state"] == "APPROVED":
            approved = True
        else:
            return False
    

    return approved
    

if __name__ == "__main__":
    reviews = get_reviews()
    is_pr_approved = has_all_reviewers_approved(reviews)
    print_review_status(is_pr_approved)
    sys.exit(0)



    


