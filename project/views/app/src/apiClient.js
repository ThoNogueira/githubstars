import axios from "axios";

const client = axios.create({
  json: true
});

class APIClient {
  loadAllRepositories(gitLogin) {
    console.log(gitLogin)
    return this.perform("post", '/api/v1/repositories', {gitLogin: gitLogin});
  }

  updateRepositoryTags(repositoryID, tags) {
    return this.perform("patch", `/api/v1/repositories/${repositoryID}`, { tags: tags });
  }

  getRepositories(gitLogin, tags) {
    return this.perform(
      "get", `/api/v1/repositories?git_login=${gitLogin}&tags=${encodeURIComponent(tags)}`
    );
  }

  getRepositoryTags(repositoryID) {
    return this.perform("get", `/api/v1/repositories/${repositoryID}/tags`);
  }

  perform(method, resource, data) {
    return client({
        method,
        url: resource,
        data
      })
      .then(response => {
        console.log(response.data)
        return response.data ? response.data : [];
      });
  }
}

export default APIClient;