<script setup lang="ts">
import CapturedPieces from './components/CapturedPieces.vue';
import ChessBoard from './components/ChessBoard.vue';

</script>

<template>
  <ChessBoard />
  <CapturedPieces />
  <router-view />
</template>

<style scoped></style>
