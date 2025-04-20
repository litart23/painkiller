<template>
  <div class="min-h-screen bg-[#FAFAFA] font-sans">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
      <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-[#1C2B3A]">Pain Library</h1>
          <p class="text-gray-500 text-sm">Real problems. Real projects.</p>
        </div>
        <button 
          @click="showModal = true"
          class="bg-[#F5F5DC] text-[#1C2B3A] px-6 py-2 rounded-lg font-medium hover:shadow-md transition-all duration-200 transform hover:scale-105 whitespace-nowrap cursor-pointer !rounded-button"
        >
          <i class="fas fa-plus-circle mr-2"></i>
          Share Your Pain
        </button>
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
            <h3 class="text-lg font-semibold text-[#1C2B3A] mb-2">{{ pain.title }}</h3>
            <p class="text-gray-700 mb-6">{{ pain.description }}</p>
            <div class="flex items-center justify-between">
              <button 
                @click="handleVote(pain.id)"
                class="flex items-center text-[#1C2B3A] hover:text-[#FFE4E1] transition-colors cursor-pointer !rounded-button whitespace-nowrap"
              >
                <i class="fas fa-fire text-[#F5F5DC] hover:text-[#FFE4E1] text-xl mr-2 transition-all duration-200"></i>
                <span>I feel this pain</span>
              </button>
              <div class="bg-[#F5F5DC] px-3 py-1 rounded-full text-[#1C2B3A] font-medium">
                {{ pain.votes }} <span class="text-sm">votes</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal -->
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
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Pain {
  id: number;
  title: string;
  description: string;
  votes: number;
}

const showModal = ref(false)
const title = ref('')
const description = ref('')
const pains = ref<Pain[]>([
  { id: 1, title: 'Slow API Response Times', description: 'Our third-party payment API is taking 3-5 seconds to respond, causing user dropoff during checkout.', votes: 42 },
  { id: 2, title: 'User Onboarding Confusion', description: 'New users are getting lost during the onboarding process and abandoning signup.', votes: 37 },
  { id: 3, title: 'Mobile Responsiveness Issues', description: 'Our dashboard breaks on smaller screens, making it unusable for mobile users.', votes: 29 },
  { id: 4, title: 'Integration Complexity', description: 'Connecting our system with legacy databases requires too much custom code.', votes: 23 },
  { id: 5, title: 'Search Performance', description: 'Search results take too long to load when the database grows beyond 10,000 records.', votes: 18 },
  { id: 6, title: 'User Permission Management', description: 'Managing role-based access control is becoming increasingly complex as we add more features.', votes: 15 },
])

const handleSubmit = () => {
  if (title.value.trim() && description.value.trim()) {
    const newPain = {
      id: pains.value.length > 0 ? Math.max(...pains.value.map(p => p.id)) + 1 : 1,
      title: title.value,
      description: description.value,
      votes: 0
    }
    pains.value = [newPain, ...pains.value]
    title.value = ''
    description.value = ''
    showModal.value = false
  }
}

const handleVote = (id: number) => {
  const painIndex = pains.value.findIndex(pain => pain.id === id)
  if (painIndex !== -1) {
    pains.value[painIndex] = {
      ...pains.value[painIndex],
      votes: pains.value[painIndex].votes + 1
    }
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