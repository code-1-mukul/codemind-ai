from pathlib import Path

from git import Repo
from git.exc import GitCommandError
from app.core.logger import logger


class RepositoryService:

    @staticmethod
    def clone_repository(repo_url: str, upload_dir: str):

        repo_name = repo_url.rstrip("/").split("/")[-1]

        destination = Path(upload_dir) / repo_name

        if destination.exists():
            return {
                "success": False,
                "message": "Repository already exists.",
                "repository_name": repo_name,
            }

        try:

            logger.info(f"Cloning repository: {repo_url}")

            Repo.clone_from(repo_url, destination)

            return {
                "success": True,
                "message": "Repository cloned successfully.",
                "repository_name": repo_name,
            }

            logger.info(f"Repository cloned: {repo_name}")

        except GitCommandError as e:

            return {
                "success": False,
                "message": f"Git clone failed: {e}",
                "repository_name": repo_name,
            }

        except Exception as e:

            logger.error(e)

            return {
                "success": False,
                "message": str(e),
                "repository_name": repo_name,
            }