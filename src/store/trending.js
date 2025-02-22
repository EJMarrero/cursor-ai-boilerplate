import { defineStore } from 'pinia'
import axios from 'axios'

export const useTrendingStore = defineStore('trending', {
  state: () => ({
    topics: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchTrending() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(`/api/trending`)
        this.topics = [...response.data];
        console.log("🚀 ~ fetchTrending ~ response:", response);
      } catch (err) {
        console.error('Error al obtener trending topics:', err);
        this.error = 'Error al cargar trending topics.';
      } finally {
        this.loading = false;
      }
    }
  }
}); 