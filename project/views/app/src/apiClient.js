import axios from "axios";

const client = axios.create({
  json: true
});

class APIClient {
  loadAllRepositories(gitLogin) {
    return this.perform("post", `/api/v1/repositories/${gitLogin}`);
  }

  updateRepositoryTags(repoID, tags) {
    return this.perform("patch", `/api/v1/repositories/${repoID}`, { tags: tags });
  }

  getRepositories(gitLogin, tags) {
    console.log("TESTE:")
    console.log(encodeURIComponent(tags))
    return this.perform(
      "get", `/api/v1/repositories?git_login=${gitLogin}&tags=${encodeURIComponent(tags)}`
    );
  }

  getRepositoryTags(repoID) {
    return this.perform("get", `/api/v1/repositories/${repoID}/tags`);
  }

  perform(method, resource, data) {
    return client({
        method,
        url: resource,
        data
      })
      .then(resp => {
        return resp.data ? resp.data : [];
      });
  }
}

export default APIClient;