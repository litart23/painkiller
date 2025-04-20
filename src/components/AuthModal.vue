<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-xl shadow-lg max-w-md w-full p-6 animate-fade-in">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-[#1C2B3A]">{{ isLogin ? 'Login' : 'Register' }}</h2>
        <button 
          @click="handleClose"
          class="text-gray-500 hover:text-gray-700 cursor-pointer"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label for="username" class="block text-gray-700 mb-2">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1C2B3A] focus:border-transparent"
            required
          />
        </div>
        <div v-if="!isLogin" class="mb-4">
          <label for="email" class="block text-gray-700 mb-2">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1C2B3A] focus:border-transparent"
            required
          />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-gray-700 mb-2">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1C2B3A] focus:border-transparent"
            required
          />
        </div>
        <div class="flex flex-col gap-4">
          <button 
            type="submit"
            class="w-full bg-[#1C2B3A] text-white px-6 py-2 rounded-lg hover:bg-opacity-90 transition-colors"
          >
            {{ isLogin ? 'Login' : 'Register' }}
          </button>
          <button 
            type="button"
            @click="toggleAuthMode"
            class="text-[#1C2B3A] hover:underline"
          >
            {{ isLogin ? 'Need an account? Register' : 'Already have an account? Login' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps<{
  show: boolean
}>()

const emit = defineEmits(['close', 'auth-success'])

const isLogin = ref(true)
const username = ref('')
const email = ref('')
const password = ref('')

const handleClose = () => {
  emit('close')
}

const toggleAuthMode = () => {
  isLogin.value = !isLogin.value
}

const handleSubmit = async () => {
  try {
    if (isLogin.value) {
      const response = await axios.post('/api/token', {
        username: username.value,
        password: password.value
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      console.log('Login response:', response.data)
      localStorage.setItem('token', response.data.access_token)
    } else {
      const registerResponse = await axios.post('/api/register', {
        username: username.value,
        email: email.value,
        password: password.value
      })
      console.log('Register response:', registerResponse.data)
      
      // After registration, automatically log in
      const loginResponse = await axios.post('/api/token', {
        username: username.value,
        password: password.value
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      console.log('Auto login response:', loginResponse.data)
      localStorage.setItem('token', loginResponse.data.access_token)
    }
    
    // Очищаем форму
    username.value = ''
    email.value = ''
    password.value = ''
    
    emit('auth-success')
    emit('close')
  } catch (error: any) {
    console.error('Authentication error:', error)
    console.error('Error details:', {
      status: error.response?.status,
      data: error.response?.data,
      headers: error.response?.headers
    })
    const errorMessage = error.response?.data?.detail || 'Произошла ошибка при аутентификации'
    alert(errorMessage)
  }
}
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