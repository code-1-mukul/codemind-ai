from pydantic import BaseModel, HttpUrl, field_validator


class RepositoryCloneRequest(BaseModel):

    repo_url: HttpUrl

    @field_validator("repo_url")
    @classmethod
    def validate_github_url(cls, value):

        if value.host != "github.com":

            raise ValueError("Only GitHub repositories are supported.")

        return value


class RepositoryCloneResponse(BaseModel):

    success: bool

    message: str

    repository_name: str