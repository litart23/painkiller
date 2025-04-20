<template>
  <div class="min-h-screen bg-[#FAFAFA] font-sans">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
      <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-[#1C2B3A]">Pain Library</h1>
          <p class="text-gray-500 text-sm">Real problems. Real projects.</p>
        </div>
        <div class="flex items-center gap-4">
          <template v-if="currentUser">
            <div class="flex items-center gap-2">
              <i class="fas fa-user text-[#1C2B3A]"></i>
              <span class="text-[#1C2B3A]">{{ currentUser.username }}</span>
            </div>
            <button 
              @click="handleLogout"
              class="text-[#1C2B3A] hover:underline"
            >
              Logout
            </button>
          </template>
          <template v-else>
            <button 
              @click="showAuthModal = true"
              class="bg-[#F5F5DC] text-[#1C2B3A] px-6 py-2 rounded-lg font-medium hover:shadow-md transition-all duration-200 transform hover:scale-105"
            >
              Sign In / Register
            </button>
          </template>
          <button 
            v-if="currentUser"
            @click="showModal = true"
            class="bg-[#F5F5DC] text-[#1C2B3A] px-6 py-2 rounded-lg font-medium hover:shadow-md transition-all duration-200 transform hover:scale-105 whitespace-nowrap cursor-pointer !rounded-button"
          >
            <i class="fas fa-plus-circle mr-2"></i>
            Share Your Pain
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto pt-24 pb-16 px-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="pain in pains" 
          :key="pain.id"
          class="bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200 transform hover:translate-y-[-4px] overflow-hidden"
        >
          <div class="p-6">
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-lg font-semibold text-[#1C2B3A]">{{ pain.title }}</h3>
              <span class="text-sm text-gray-500">by {{ pain.user.username }}</span>
            </div>
            <p class="text-gray-700 mb-6">{{ pain.description }}</p>
            <div class="flex items-center justify-between">
              <button 
                @click="handleVote(pain.id)"
                :disabled="!currentUser"
                :class="[
                  'flex items-center transition-colors cursor-pointer !rounded-button whitespace-nowrap',
                  currentUser ? 'text-[#1C2B3A] hover:text-[#FFE4E1]' : 'text-gray-400 cursor-not-allowed'
                ]"
              >
                <i class="fas fa-fire text-[#F5F5DC] hover:text-[#FFE4E1] text-xl mr-2 transition-all duration-200"></i>
                <span>I feel this pain</span>
              </button>
              <div class="bg-[#F5F5DC] px-3 py-1 rounded-full text-[#1C2B3A] font-medium">
                {{ pain.votes_count }} <span class="text-sm">votes</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Create Pain Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-xl shadow-lg max-w-md w-full p-6 animate-fade-in">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-[#1C2B3A]">Share Your Pain</h2>
            <button 
              @click="showModal = false"
              class="text-gray-500 hover:text-gray-700 cursor-pointer !rounded-button whitespace-nowrap"
            >
              <i class="fas fa-times"></i>
            </button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="mb-4">
              <label for="title" class="block text-gray-700 mb-2">Title</label>
              <input
                type="text"
                id="title"
                v-model="title"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1C2B3A] focus:border-transparent"
                placeholder="What's the pain point?"
                required
              />
            </div>
            <div class="mb-6">
              <label for="description" class="block text-gray-700 mb-2">Description</label>
              <textarea
                id="description"
                v-model="description"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1C2B3A] focus:border-transparent h-32 resize-none"
                placeholder="Describe the problem in detail..."
                required
              ></textarea>
            </div>
            <div class="flex justify-end gap-3">
              <button 
                type="button" 
                @click="showModal = false"
                class="px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors cursor-pointer !rounded-button whitespace-nowrap"
              >
                Cancel
              </button>
              <button 
                type="submit"
                class="bg-[#1C2B3A] text-white px-6 py-2 rounded-lg hover:bg-opacity-90 transition-colors cursor-pointer !rounded-button whitespace-nowrap"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Auth Modal -->
    <AuthModal 
      :show="showAuthModal"
      @close="showAuthModal = false"
      @auth-success="handleAuthSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AuthModal from './components/AuthModal.vue'

interface User {
  id: number;
  username: string;
  email: string;
}

interface Pain {
  id: number;
  title: string;
  description: string;
  user: User;
  votes_count: number;
}

const showModal = ref(false)
const showAuthModal = ref(false)
const title = ref('')
const description = ref('')
const pains = ref<Pain[]>([])
const currentUser = ref<User | null>(null)

const fetchPains = async () => {
  try {
    const response = await axios.get('/api/pains')
    pains.value = response.data
  } catch (error) {
    console.error('Error fetching pains:', error)
  }
}

const fetchCurrentUser = async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const response = await axios.get('/api/users/me', {
        headers: { Authorization: `Bearer ${token}` }
      })
      currentUser.value = response.data
    } catch (error) {
      console.error('Error fetching current user:', error)
      localStorage.removeItem('token')
      currentUser.value = null
    }
  }
}

const handleSubmit = async () => {
  if (title.value.trim() && description.value.trim()) {
    try {
      const token = localStorage.getItem('token')
      await axios.post('/api/pains', {
        title: title.value,
        description: description.value
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      title.value = ''
      description.value = ''
      showModal.value = false
      await fetchPains()
    } catch (error) {
      console.error('Error creating pain:', error)
      alert(error.response?.data?.detail || 'An error occurred')
    }
  }
}

const handleVote = async (painId: number) => {
  if (!currentUser.value) {
    showAuthModal.value = true
    return
  }

  try {
    const token = localStorage.getItem('token')
    await axios.post('/api/votes', {
      pain_id: painId
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    await fetchPains()
  } catch (error) {
    console.error('Error voting:', error)
    alert(error.response?.data?.detail || 'An error occurred')
  }
}

const handleAuthSuccess = async () => {
  await fetchCurrentUser()
  await fetchPains()
}

const handleLogout = () => {
  localStorage.removeItem('token')
  currentUser.value = null
}

onMounted(async () => {
  await fetchCurrentUser()
  await fetchPains()
})

// Настраиваем axios для автоматического добавления токена
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.3s ease-out forwards;
}
</style> 