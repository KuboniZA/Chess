<script setup lang="ts">
import { ref, onMounted, } from 'vue';

// captured pieces display
const whiteCapturedPieces = ref<string[]>([]);
const blackCapturedPieces = ref<string[]>([]);

const fetchCapturedPieces = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/captured-pieces', {
      method: 'GET',
    });
    const data = await response.json();
    whiteCapturedPieces.value = data['captured-pieces'].white;
    blackCapturedPieces.value = data['captured-pieces'].black;
    console.log('Fetched captured pieces:', data);
  } catch (error) {
    console.error('Error fetching captured pieces:', error);
  }
};

onMounted(() => {
  fetchCapturedPieces();
});
</script>

<template>
   <h3 class="captured-title">White Captured Pieces </h3>
   <div v-for="piece in whiteCapturedPieces" :key="piece" class="captured wp">
      {{ piece }}
    </div>
    <h3 class="captured-title t2">Black Captured Pieces</h3>
   <div v-for="piece in blackCapturedPieces" :key="piece" class="captured bp">
      {{ piece }}
    </div>
</template>

<style scoped>
  .captured-title {
  position: absolute;
  top: 3%;
  left: 7%;
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}
.captured-title.t2 {
  left: 80%;
}

.captured {
  position: absolute;
  top: 9%;
  font-size: 3.5rem;
  user-select: none;
}

</style>
