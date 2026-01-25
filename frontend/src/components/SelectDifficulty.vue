<script setup lang="ts">
  import {ref, onMounted } from 'vue';
  type Difficulty = 'beginner' | 'intermediate' | 'advanced';

  const emit = defineEmits<{
    (e: 'selected', difficulty: Difficulty): void;
  }>();

  const selectedDifficulty = ref<Difficulty>('beginner')

  onMounted(async () => {
    const response = await fetch('http://127.0.0.1:5000/game-mode');
    const data = await response.json();
    selectedDifficulty.value = data.difficulty
  })

  async function confirmSelection() {
    await fetch('http://127.0.0.1:5000/game-mode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }, // research headers man
      body: JSON.stringify({
        difficulty: selectedDifficulty.value
      })
    });
    emit('selected', selectedDifficulty.value)
  }


</script>

<template>
  <div class="diff-modal">
    <div class="diff-content">
      <h2>Wlecome to Chessmate!</h2>
      <p>Please select your difficulty:</p>
      <select v-model="selectedDifficulty">
        <option value="beginner">Beginner</option>
        <!-- <option>Beginner with Clock</option> -->
        <option value="intermediate">Intermediate</option>
        <!-- <option>Intermediate with Clock</option> -->
        <option value="advanced">Hard</option>
        <!-- <option>Hard with Clock</option> -->
      </select>
      <button @click="confirmSelection">Start Game</button>
    </div>
  </div>

</template>

<style scoped>
.diff-modal {
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

.diff-content {
  background-color: white;
  padding: 2rem;
  border-radius: 0.5rem;
  position: relative;
  text-align: center;
  align-items: center;
  width: 60%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}
p { margin-bottom: 2rem; }
button {
  width: 8rem;
  height: 2.5rem;
  margin-bottom: 0.75rem;
  border-radius: 1000px;
  border: none;
  position: relative;
  left: 25%;
  top: -3.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);

}
button:hover {
  cursor: pointer;
  background-color: aquamarine;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}
select {
  width: 10rem;
  height: 2.5rem;
  font-size: 1rem;
  position: relative;
  left: 4rem;

}
</style>
