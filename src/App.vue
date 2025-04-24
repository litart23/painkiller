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
              <span class="text-[#1C2B3A]">{{ currentUser?.username || 'Unknown' }}</span>
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
              <h3 class="text-lg font-semibold text-[#1C2B3A]">{{ pain.title.substring(0,100) }}</h3>
              <span class="text-sm text-gray-500">by {{ pain.user?.username || 'Unknown' }} </span>
            </div>
            <p class="text-gray-700 mb-6">{{ pain.description.substring(0,100) }}</p>
            <div class="flex items-center justify-between mb-2">
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
                {{ pain.votes_count || 0 }} <span class="text-sm">votes</span>
              </div>
            </div>
              <div class="flex justify-end ">
                <p class="text-sm text-gray-500">created at {{ pain.created_at.substring(0,10) }}</p>
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

// Настраиваем axios
axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.withCredentials = false  // Отключаем credentials
axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Accept'] = 'application/json'

// Настраиваем axios для автоматического добавления токена
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  console.log('Request config:', config)
  return config
}, error => {
  console.error('Request error:', error)
  return Promise.reject(error)
})

// Добавляем обработчик ошибок
axios.interceptors.response.use(
  response => {
    console.log('Response:', response)
    return response
  },
  error => {
    console.error('Response error:', error)
    console.error('Response error details:', {
      status: error.response?.status,
      data: error.response?.data,
      headers: error.response?.headers
    })
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      currentUser.value = null
    }
    return Promise.reject(error)
  }
)

interface User {
  id: number;
  username: string;
  email: string;
}

interface Pain {
  id: number;
  title: string;
  description: string;
  created_at: string;
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
    console.log('Fetching pains...')
    const response = await axios.get('/api/pains')
    console.log('Raw pains response:', response)
    console.log('Pains data structure:', JSON.stringify(response.data, null, 2))
    
    // Проверяем и преобразуем данные, если нужно
    pains.value = response.data.map((pain: any) => ({
      id: pain.id,
      title: pain.title,
      description: pain.description,
      created_at: pain.created_at,
      user: {
        id: pain.user_id,
        username: pain.creator?.username || pain.user?.username || 'Unknown',
        email: pain.creator?.email || pain.user?.email || ''
      },
      votes_count: pain.votes_count || 0
    }))
    
    console.log('Processed pains:', pains.value)
  } catch (error: any) {
    console.error('Error fetching pains:', error)
    console.error('Error details:', {
      status: error.response?.status,
      data: error.response?.data,
      headers: error.response?.headers
    })
  }
}

const fetchCurrentUser = async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      console.log('Fetching current user...')
      const response = await axios.get('/api/users/me', {
        headers: { Authorization: `Bearer ${token}` }
      })
      console.log('Raw current user response:', response)
      console.log('Current user data structure:', JSON.stringify(response.data, null, 2))
      
      currentUser.value = {
        id: response.data.id,
        username: response.data.username,
        email: response.data.email
      }
      
      console.log('Processed current user:', currentUser.value)
    } catch (error: any) {
      console.error('Error fetching current user:', error)
      console.error('Error details:', {
        status: error.response?.status,
        data: error.response?.data,
        headers: error.response?.headers
      })
      localStorage.removeItem('token')
      currentUser.value = null
    }
  }
}

const handleSubmit = async () => {
  if (!title.value.trim() || !description.value.trim()) {
    alert('Пожалуйста, заполните все поля')
    return
  }

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      showAuthModal.value = true
      return
    }

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
  } catch (error: any) {
    console.error('Error creating pain:', error)
    if (error.response?.status === 401) {
      showAuthModal.value = true
    } else {
      alert(error.response?.data?.detail || 'Произошла ошибка при создании записи')
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
    if (!token) {
      showAuthModal.value = true
      return
    }

    await axios.post('/api/votes', {
      pain_id: painId
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    await fetchPains()
  } catch (error: any) {
    console.error('Error voting:', error)
    if (error.response?.status === 401) {
      showAuthModal.value = true
    } else if (error.response?.status === 400) {
      alert('Вы уже проголосовали за эту запись')
    } else {
      alert(error.response?.data?.detail || 'Произошла ошибка при голосовании')
    }
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