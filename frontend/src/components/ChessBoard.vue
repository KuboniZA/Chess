<script setup lang="ts">
import { ref, onMounted } from 'vue';

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
</script>

<template>
   <div class="chess-board-container">
     <div v-for="(_, index) in 64" :key="index" class="square" :class="{ dark: isDark(index) }">
      <span v-if="pieceAt(index)" class="piece" :class="pieceAt(index)!.color">{{ pieceSymbol(pieceAt(index)!) }}</span>
      <small class="coord">{{ indexToSquare(index) }}</small>
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

.coord {
  position: absolute;
  font-size: 0.6rem;
  color: red;
  bottom: 2px;
  right: 2px;
}


/* Adjusted positions by 5.7 for better vertical alignment */
/* .pawn1 { left: 29.3rem }
.pawn2 { left: 35rem; }
.pawn3 { left: 40.7rem; }
.pawn4 { left: 46.2rem; }
.pawn5 { left: 51.9rem; }
.pawn6 { left: 57.6rem; }
.pawn7 { left: 63.3rem; }
.pawn8 { left: 69rem; }

.queen { left: 45.9rem; }
.bishop1 { left: 40.2rem; }
.knight1 { left: 34.5rem; }
.rook1 { left: 28.8rem; }

.king { left: 51.6rem; }
.rook2 { left: 68.7%; }
.bishop2 { left: 57.3rem; }
.knight2 { left: 63rem; }

.pawns {
  position: absolute;
  font-size: 3rem;
  top: 9.2rem;
}

.ryl-pcs {
  position: absolute;
  font-size: 4rem;
  top: 2.7rem;
}
.w-pawn1 { left: 29.3rem }
.w-pawn2 { left: 35rem; }
.w-pawn3 { left: 40.7rem; }
.w-pawn4 { left: 46.2rem; }
.w-pawn5 { left: 51.9rem; }
.w-pawn6 { left: 57.6rem; }
.w-pawn7 { left: 63.3rem; }
.w-pawn8 { left: 69rem; }

.w-queen { left: 45.9rem; }
.w-bishop1 { left: 40.2rem; }
.w-knight1 { left: 34.5rem; }
.w-rook1 { left: 28.8rem; }

.w-king { left: 51.6rem; }
.w-rook2 { left: 68.7%; }
.w-bishop2 { left: 57.3rem; }
.w-knight2 { left: 63rem; }

.w-pawns {
  position: absolute;
  font-size: 3rem;
  top: 37.2rem;
  color: white;
}

.w-ryl-pcs {
  position: absolute;
  font-size: 4rem;
  top: 42.5rem;
  color: white;
} */
</style>
