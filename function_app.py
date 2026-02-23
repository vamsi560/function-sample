import logging
import requests
import os
import azure.functions as func

app = func.FunctionApp()

@app.route(route="http_trigger1", auth_level=func.AuthLevel.FUNCTION)
def http_trigger1(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = req.get_json()

        pr_id = payload.get("pullRequest", {}).get("id")
        branch = payload.get("pullRequest", {}).get("fromRef", {}).get("displayId")
        repo_name = payload.get("repository", {}).get("slug")

        github_token = os.environ["GITHUB_TOKEN"]
        owner = os.environ["GITHUB_OWNER"]
        repo = os.environ["GITHUB_REPO"]

        url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/pr-test.yml/dispatches"

        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json"
        }

        data = {
            "ref": "main",
            "inputs": {
                "pr_id": str(pr_id),
                "branch": branch,
                "repo_name": repo_name
            }
        }

        response = requests.post(url, headers=headers, json=data)

        return func.HttpResponse(
            f"GitHub trigger response: {response.status_code}",
            status_code=200
        )

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("Error occurred", status_code=500)
