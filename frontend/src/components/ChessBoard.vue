<script setup lang="ts">
const isDark = (n: number) => {
  const row = Math.floor((n - 1) / 8);
  const col = (n - 1) % 8;
  return (row + col) % 2 === 1;
};
</script>
<template>
   <div class="chess-board-container">
     <div v-for="n in 64" :key="n" class="square" :class="{ dark: isDark(n) }"></div>
   </div>
</template>

<style scoped>
.chess-board-container {
  display: grid;
  width: 45rem;
  height: 45rem;
  background-color: #f0d9b5;
  border: 2px solid #7e4e27;
  grid-template-columns: repeat(8, 1fr);
  grid-template-rows: repeat(8, 1fr);
  position: relative;
  top: 2rem;
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}

.square {
  background: #f0d9b5;
}

.square.dark {
  background: #b58863;
}
</style>
