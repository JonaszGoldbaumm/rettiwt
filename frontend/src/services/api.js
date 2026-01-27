const BASE_URL = 'http://localhost:8080';

export const apiFetch = async (endpoint, options = {}, token = null) => {
  const headers = { ...options.headers };


  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  if (token) headers['Authorization'] = `Bearer ${token}`;

  const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    let errorMsg = 'Request failed';
    try {
      const error = await response.json();
      errorMsg = error.detail || error.message || errorMsg;
    } catch {}
    throw new Error(errorMsg);
  }

  return response.json();
};