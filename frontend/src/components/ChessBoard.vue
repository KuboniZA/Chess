<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Piece visibility and positions

type Piece = {
  type: string;
  color: 'white' | 'black';
  position: string;
};

const pieces = ref<Piece[]>([]);

const fetchPieces = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/board');
    const data = await response.json();
    pieces.value = data.board_state;
    console.log('Fetched pieces:', pieces.value);
  } catch (error) {
    console.error('Error fetching pieces:', error);
  }
};

onMounted(() => {
  fetchPieces();
});

const isDark = (index: number) => {
  const row = Math.floor(index / 8);
  const col = index % 8;
  return (row + col) % 2 === 1;
};

const indexToSquare = (index: number) => {
  const file = String.fromCharCode(97 + (index % 8)); // 'a' to 'h'
  const rank = 8 - Math.floor(index / 8); // '1' to '8'
  return `${file}${rank}`;
};

const pieceAt = (index: number) => {
  const square = indexToSquare(index);
  return pieces.value.find(piece => piece.position === square);
};

const pieceSymbol = (piece: Piece) => {
  const symbols: Record<string, string> = {
    'p': piece.color === 'white' ? '♙' : '♟', // Pawn
    'r': piece.color === 'white' ? '♖' : '♜', // Rook
    'n': piece.color === 'white' ? '♘' : '♞', // Knight
    'b': piece.color === 'white' ? '♗' : '♝', // Bishop
    'q': piece.color === 'white' ? '♕' : '♛', // Queen
    'k': piece.color === 'white' ? '♔' : '♚', // King
  };
  return symbols[piece.type];
};

// Code for handling piece movement

const selectedPiece = ref<Piece | null>(null);
const selectedSquare = ref<string | null>(null);

const onSquareClick = async (index: number) => {
  const square = indexToSquare(index);
  const piece = pieceAt(index);

  if (!selectedSquare.value) {
    // Select a piece
    if (piece) {
      selectedPiece.value = piece;
      selectedSquare.value = square;
    }
    return;
  } if (selectedSquare.value === square) {
    // Deselect the piece
    selectedPiece.value = null;
    selectedSquare.value = null;
    return;
  }
  // Move the piece
  await movePiece(selectedSquare.value, square);
  selectedPiece.value = null;
  selectedSquare.value = null;
};

const movePiece = async (from: string, to: string) => {
  const move = `${from}${to}`;

  const response = await fetch('http://127.0.0.1:5000/move', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ move }),
  });

  const data = await response.json();
  if (data.status === 'success') {
    // Update the board state
    pieces.value = data.board_state;
  } else {
    console.error('Invalid move:', data.message);
  }
};

</script>

<template>
   <div class="chess-board-container">
     <div v-for="(_, index) in 64" :key="index" class="square" :class="{ dark: isDark(index), selected: selectedSquare === indexToSquare(index) }" @click="onSquareClick(index)">
      <span v-if="pieceAt(index)" class="piece" :class="pieceAt(index)!.color">{{ pieceSymbol(pieceAt(index)!) }}</span>
      <!-- <small class="coord">{{ indexToSquare(index) }}</small> -->
     </div>

   </div>

   <!-- <div class="black-pieces">
    <span class="pawns pawn1">&#9823;</span>
    <span class="pawns pawn2">&#9823;</span>
    <span class="pawns pawn3">&#9823;</span>
    <span class="pawns pawn4">&#9823;</span>
    <span class="pawns pawn5">&#9823;</span>
    <span class="pawns pawn6">&#9823;</span>
    <span class="pawns pawn7">&#9823;</span>
    <span class="pawns pawn8">&#9823;</span>

    <span class="ryl-pcs king">&#9818;</span>
    <span class="ryl-pcs queen">&#9819;</span>
    <span class="ryl-pcs rook1">&#9820;</span>
    <span class="ryl-pcs rook2">&#9820;</span>
    <span class="ryl-pcs bishop1">&#9821;</span>
    <span class="ryl-pcs bishop2">&#9821;</span>
    <span class="ryl-pcs knight1">&#9822;</span>
    <span class="ryl-pcs knight2">&#9822;</span>
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

    <span class="w-ryl-pcs w-king">&#9818;</span>
    <span class="w-ryl-pcs w-queen">&#9819;</span>
    <span class="w-ryl-pcs w-rook1">&#9820;</span>
    <span class="w-ryl-pcs w-rook2">&#9820;</span>
    <span class="w-ryl-pcs w-bishop1">&#9821;</span>
    <span class="w-ryl-pcs w-bishop2">&#9821;</span>
    <span class="w-ryl-pcs w-knight1">&#9822;</span>
    <span class="w-ryl-pcs w-knight2">&#9822;</span>
   </div> -->
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
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8)0;
}

.square {
  position: relative;
  background: #f0d9b5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3.5rem;
}

.square.dark {
  background: #b58863;
}

.piece {
  cursor: pointer;
  font-size: 3.5rem;
  user-select: none;
  z-index: 1;
}
.piece.white {
  color: white;
}
.piece.black {
  color: black;
}

.square.selected {
  outline: 3px solid #3b82f6;
  outline-offset: -3px;
}


/* .coord {
  position: absolute;
  font-size: 0.6rem;
  color: red;
  bottom: 2px;
  right: 2px;
} */


</style>
