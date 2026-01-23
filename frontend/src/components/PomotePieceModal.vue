<script setup lang="ts">

  type PromotionPiece = 'q' | 'r' | 'b' | 'n';

  const emit = defineEmits<{
    (e: 'select', piece: PromotionPiece): void;
  }>();

  const pieces: { code: PromotionPiece; symbol: string; label: string }[] = [
  { code: 'q', symbol: '♕', label: 'Queen' },
  { code: 'r', symbol: '♖', label: 'Rook' },
  { code: 'b', symbol: '♗', label: 'Bishop' },
  { code: 'n', symbol: '♘', label: 'Knight' },
];
</script>

<template>
  <div class="modal-backdrop">
    <div class="modal">
      <h3>Promote pawn to:</h3>
      <div class="choices">
        <button v-for="p in pieces" :key="p.code" @click="emit('select', p.code)" class="choice">
          {{ p.symbol }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #f0d9b5;
  padding: 1.5rem;
  border-radius: 0.5rem;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}

.choices {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.choice {
  font-size: 3rem;
  cursor: pointer;
  background: none;
  border: none;
}
</style>
