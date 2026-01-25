<script setup lang="ts"></script>

<template>
  <div class="diff-modal">
    <div class="diff-content">
      <h2>Wlecome to Chessmate!</h2>
      <p>Please select your difficulty:</p>
      <button>Beginner</button><br/>
      <button>Beginner with Clock</button><br/>
      <button>Intermediate</button><br/>
      <button>Intermediate with Clock</button><br/>
      <button>Hard</button><br/>
      <button>Hard with Clock</button><br/>
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
  width: 60%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}
p { margin-bottom: 2rem; }
button {
  width: 12rem;
  height: 3rem;
  margin-bottom: 0.75rem;
  border-radius: 1000px;
  border: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}
button:hover {
  cursor: pointer;
  background-color: aquamarine;
}
</style>
