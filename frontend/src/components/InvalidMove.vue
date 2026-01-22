<script setup lang="ts">
// Invalid move modal component
defineProps({
  message: { type: String, default: null },
});

defineEmits(['close']);
</script>

<template>
  <div class="invalid-move-modal">
    <div v-if="message" class="modal-content">
      <h2>Try again:</h2>
      <p>{{ message }}</p>
      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<style scoped>
  .invalid-move-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 0.5rem;
  position: relative;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}
</style>
