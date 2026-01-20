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

   <div class="black-pieces">
    <span class="pawns pawn1">&#9823;</span>
    <span class="pawns pawn2">&#9823;</span>
    <span class="pawns pawn3">&#9823;</span>
    <span class="pawns pawn4">&#9823;</span>
    <span class="pawns pawn5">&#9823;</span>
    <span class="pawns pawn6">&#9823;</span>
    <span class="pawns pawn7">&#9823;</span>
    <span class="pawns pawn8">&#9823;</span>
   </div>
   <div class="white-pieces">
    <span class="w-pawns w-pawn1">&#9823;</span>
    <span class="w-pawns w-pawn2">&#9823;</span>
    <span class="w-pawns w-pawn3">&#9823;</span>
    <span class="w-pawns w-pawn4">&#9823;</span>
    <span class="w-pawns w-pawn5">&#9823;</span>
    <span class="w-pawns w-pawn6">&#9823;</span>
    <span class="w-pawns w-pawn7">&#9823;</span>
    <span class="w-pawns w-pawn8">&#9823;</span>
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
.pawn1 { left: 29.3rem }
.pawn2 { left: 35rem; }
.pawn3 { left: 40.7rem; }
.pawn4 { left: 46.2rem; }
.pawn5 { left: 51.9rem; }
.pawn6 { left: 57.6rem; }
.pawn7 { left: 63.3rem; }
.pawn8 { left: 69rem; }

.pawns {
  position: absolute;
  font-size: 3rem;
  top: 9.2rem;
}
.w-pawn1 { left: 29.3rem }
.w-pawn2 { left: 35rem; }
.w-pawn3 { left: 40.7rem; }
.w-pawn4 { left: 46.2rem; }
.w-pawn5 { left: 51.9rem; }
.w-pawn6 { left: 57.6rem; }
.w-pawn7 { left: 63.3rem; }
.w-pawn8 { left: 69rem; }
.w-pawns {
  position: absolute;
  font-size: 3rem;
  top: 37.2rem;
  color: white;
}
</style>
