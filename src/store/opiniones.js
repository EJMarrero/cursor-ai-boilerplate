import { defineStore } from 'pinia'
import axios from 'axios'

export const useOpinionesStore = defineStore('opiniones', {
  state: () => ({
    opiniones: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchOpiniones() {
      this.loading = true
      this.error = null
      try {
        // Usar la variable de entorno para la URL del API
        /* const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/opiniones`) */
        const response = await axios.get(`/api/opiniones`)
        this.opiniones = [...response.data];
        console.log("🚀 ~ fetchOpiniones ~ response:", response)
        
      } catch (err) {
        console.error('Error al obtener opiniones:', err)
        this.error = 'Error al cargar las opiniones.'
      } finally {
        this.loading = false
      }
    }
  }
}) 