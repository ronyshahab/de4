const BASE_URL = "http://localhost:5000";

export const callApi = (method, endpoint, config = {}) => {
  const { body, headers = {} } = config;

  return fetch(BASE_URL + endpoint, {
    method,
    body,
    headers,
  })
    .then(response => {
      if (response.ok) return response.text();
      throw new Error("Upload failed");
    })
    .then(result => {
      return result;
    })
    .catch(error => {
      throw error;
    });
};
