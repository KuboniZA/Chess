<script setup lang="ts">
defineProps<{
  show: boolean;
  message: 'Check' | 'Checkmate'
}>();
</script>

<template>
  <transition>
    <div v-if="show" class="check">
      <span v-if="message === 'Check'">{{ message }}: Protect your king!</span>
      <span v-else>{{ message }}: Game Over!</span>
    </div>
  </transition>

</template>

<style scoped>
.check {
  position: absolute;
  color: red;
  top: 50%;
  left: 80%;
  transform: translateY(-50%);
  padding: 0.75rem 1.25rem;
  background: #e63947da;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  z-index: 100;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}

/* tiny pop animation */
.pop-enter-active,
.pop-leave-active {
  transition: all 0.2s ease;
}
.pop-enter-from,
.pop-leave-to {
  opacity: 0;
  transform: translateX(-50%) scale(0.95);
}

</style>
