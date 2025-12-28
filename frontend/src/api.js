import axios from 'axios'

// Use Vite env variable (VITE_API_URL) if provided; otherwise use proxied '/api' in dev or default to localhost for production
const viteApi = import.meta.env.VITE_API_URL || ''
const base = viteApi || (import.meta.env.DEV ? '/api' : 'http://localhost:8000/api')
const api = axios.create({ baseURL: base })
export default api
