<script setup lang="ts">
  import { ref } from 'vue';
  type Difficulty = 'beginner' | 'intermediate' | 'advanced';
  type PlayerType = 'human' | 'ai'

  const emit = defineEmits<{
    (e: 'start-game', payload: {
      white: PlayerType;
      black: PlayerType;
      difficulty: Difficulty;
    }): void;
  }>();

  const selectedDifficulty = ref<Difficulty>('beginner');
  const whitePlayer = ref<PlayerType>('human');
  const blackPlayer = ref<PlayerType>('ai');


  // onMounted(async () => {
  //   const response = await fetch('http://127.0.0.1:5000/game-mode');
  //   const data = await response.json();
  //   selectedDifficulty.value = data.difficulty
  // })

  async function startGame() {
    // Validate that there's at least one human
    if (whitePlayer.value === 'ai' && blackPlayer.value === 'ai') {
      alert('At least one player must be human');
      return;
    }

    await fetch('http://127.0.0.1:5000/game-mode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }, // research headers man
      body: JSON.stringify({
        white: whitePlayer.value,
        black: blackPlayer.value,
        difficulty: selectedDifficulty.value
      })
    });
    emit('start-game', {
      white: whitePlayer.value,
      black: blackPlayer.value,
      difficulty: selectedDifficulty.value
    })
  }


</script>

<template>
  <div class="diff-modal">
    <div class="diff-content">
      <h2>Welcome to Chessmate!</h2>

      <p>Please select your difficulty:</p>
      <!-- <select v-model="selectedDifficulty">
        <option value="beginner">Beginner</option>
        <option>Beginner with Clock</option>
        <option value="intermediate">Intermediate</option>
        <option>Intermediate with Clock</option>
        <option value="advanced">Hard</option>
        <option>Hard with Clock</option>
      </select> -->

      <!-- WILL NEED TO REFACTOR THE BELOW CODE -->

      <label>
        White:
        <select v-model="whitePlayer">
          <option value="human">Human</option>
          <option value="ai">AI</option>
        </select>
      </label>

      <label>
        Black:
        <select v-model="blackPlayer">
          <option value="human">Human</option>
          <option value="ai">AI</option>
        </select>
      </label>

      <label v-if="whitePlayer === 'ai' || blackPlayer === 'ai'">
        Computer Difficulty:
        <select v-model="selectedDifficulty">
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </label>

      <button @click="startGame">Start Game</button>
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
