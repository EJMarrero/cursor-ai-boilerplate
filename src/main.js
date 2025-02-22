import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'

// Importar estilos de TailwindCSS
import './assets/tailwind.css'

// Crear la aplicación Vue y registrar Pinia
const app = createApp(App)
app.use(createPinia())
app.mount('#app') 