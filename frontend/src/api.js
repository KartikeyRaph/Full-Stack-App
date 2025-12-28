import axios from 'axios'

// Use proxied path in development (vite proxy) or direct backend URL in production
const base = import.meta.env.DEV ? '/api' : 'http://localhost:8000/api'
const api = axios.create({ baseURL: base })
export default api
