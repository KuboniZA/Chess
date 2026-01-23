<script setup lang="ts">
import { ref, onMounted, } from 'vue';

interface CapturedPiece {
  type: string;
  color: 'white' | 'black';
  symbol: string;
}


// captured pieces display
const whiteCapturedPieces = ref<CapturedPiece[]>([]);
const blackCapturedPieces = ref<CapturedPiece[]>([]);

const fetchCapturedPieces = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/captured-pieces', {
      method: 'GET',
    });
    const data = await response.json();
    whiteCapturedPieces.value = data['white-captured'];
    blackCapturedPieces.value = data['black-captured'];
    // console.log('Fetched captured pieces:', data);
    console.log('White captured pieces:', data['white-captured']);
    console.log('Black captured pieces:', data['black-captured']);
  } catch (error) {
    console.error('Error fetching captured pieces:', error);
  }
};

const resetCapturedPieces = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/reset-captured', {
      method: 'POST',
    });
    const data = await response.json();
    console.log('Reset captured pieces:', data);
    whiteCapturedPieces.value = [];
    blackCapturedPieces.value = [];
  } catch (error) {
    console.error('Error resetting captured pieces:', error);
  }
};

onMounted(() => {
  fetchCapturedPieces();
});

defineExpose({
  fetchCapturedPieces,
  resetCapturedPieces
});

</script>

<template>
  <h3 class="captured-title">White Captured Pieces </h3>
   <div class="captured-container wp">
    <span v-for="(piece, index) in whiteCapturedPieces" :key="index" class="captured-white">
      {{ piece.symbol }}
   </span>
  </div>

  <h3 class="captured-title t2">Black Captured Pieces</h3>
   <div class="captured-container bp">
    <span v-for="(piece, index) in blackCapturedPieces" :key="index" class="captured-black">
      {{ piece.symbol }}
    </span>
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

.captured-container {
  position: absolute;
  display: flex;
  flex-wrap: wrap;
  top: 9%;
  gap: 0.5rem;
  font-size: 3.5rem;
  user-select: none;
}

.captured-container.wp {
  left: 7%;
  width: fit-content;
  height: fit-content;
}
.captured-container.bp {
  left: 80%;
  width: fit-content;
  height: fit-content;
}

</style>
