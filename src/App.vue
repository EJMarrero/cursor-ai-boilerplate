<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Panel de Análisis</h1>
    
    <!-- Navegación con tabs -->
    <div class="flex mb-4">
      <button
        :class="selectedTab === 'opiniones' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'"
        @click="selectedTab = 'opiniones'"
        class="px-4 py-2 rounded-l focus:outline-none"
      >
        Opiniones Analizadas
      </button>
      <button
        :class="selectedTab === 'trending' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800'"
        @click="selectedTab = 'trending'"
        class="px-4 py-2 rounded-r focus:outline-none"
      >
        Trending Topics
      </button>
    </div>
    
    <!-- Sección de Opiniones -->
    <div v-if="selectedTab === 'opiniones'">
      <!-- Indicador de carga -->
      <div v-if="loading" class="text-center">
        Cargando opiniones...
      </div>
      <!-- Mensaje de error -->
      <div v-if="error" class="text-red-500">
        {{ error }}
      </div>
      <!-- Listado de opiniones -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" v-if="!loading && !error">
        <ReviewCard
          v-for="opinion in opiniones"
          :key="opinion.id || opinion._id || opinion.opinion_limpia"
          :opinion="opinion"
        />
      </div>
    </div>
    
    <!-- Sección de Trending Topics -->
    <div v-if="selectedTab === 'trending'">
      <!-- Indicador de carga -->
      <div v-if="trendingLoading" class="text-center">
        Cargando trending topics...
      </div>
      <!-- Mensaje de error -->
      <div v-if="trendingError" class="text-red-500">
        {{ trendingError }}
      </div>
      <!-- Listado de trending topics -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" v-if="!trendingLoading && !trendingError">
        <TrendingCard
          v-for="topic in topics"
          :key="topic.url || topic.topic"
          :trending="topic"
        />
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useOpinionesStore } from './store/opiniones'
import { useTrendingStore } from './store/trending'
import ReviewCard from './components/ReviewCard.vue'
import TrendingCard from './components/TrendingCard.vue'

// Store de Opiniones
const opinionesStore = useOpinionesStore()
const { opiniones, loading, error } = storeToRefs(opinionesStore)
const { fetchOpiniones } = opinionesStore

// Store de Trending Topics
const trendingStore = useTrendingStore()
const { topics, loading: trendingLoading, error: trendingError } = storeToRefs(trendingStore)
const { fetchTrending } = trendingStore

// Estado para la navegación por pestañas
const selectedTab = ref('opiniones')

// Al montar el componente se obtienen ambas secciones
onMounted(() => {
  fetchOpiniones()
  fetchTrending()
  console.log("Opiniones:", opiniones.value)
  console.log("Trending Topics:", topics.value)
})
</script>

<style scoped>
/* Puedes agregar estilos adicionales aquí si lo deseas */
</style> 