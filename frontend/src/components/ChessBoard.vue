<script setup lang="ts">
import { ref, onMounted, } from 'vue';
import InvalidMove from './InvalidMove.vue';
import CapturedPieces from './CapturedPieces.vue';
import PomotePieceModal from './PomotePieceModal.vue';
import InCheck from './InCheck.vue';

// Piece visibility and positions

type Piece = {
  type: string;
  color: 'white' | 'black';
  position: string;
};

type MoveResponse = {
  status: 'success' | 'error';
  board_state?: Piece[];
  turn?: 'White' | 'Black';
  check?: boolean;
  checkmate?: boolean;
  message?: string;
};


const pieces = ref<Piece[]>([]);

const fetchPieces = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/board');
    const data = await response.json();
    pieces.value = data.board_state;
    turn.value = data.turn
    updateCheckState(data)
    console.log('Fetched pieces:', pieces.value);
  } catch (error) {
    console.error('Error fetching pieces:', error);
  }
};

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

const turn = ref<'White' | 'Black'>('White');
const errorMessage = ref<string | null>(null);
const childRef = ref<InstanceType<typeof CapturedPieces> | null>(null);

const movePiece = async (from: string, to: string) => {
  if (selectedPiece.value && isPromotionMove(selectedPiece.value, to)) {
    pendingPromotionMove.value = { from, to };
    showPromotionModal.value = true;
    return;
  }

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
    turn.value = turn.value === 'White' ? 'Black' : 'White';
    childRef.value?.fetchCapturedPieces();
    updateCheckState(data)
    // console.log('Move successful:', pieces.value);

    // Computer's turn
    if (turn.value === 'Black') {
      setTimeout(async () => {
        await fetchPieces();
        childRef.value?.fetchCapturedPieces();
      }, 1500);
    }
  } else {
    // console.error('Invalid move:', data.message);
    errorMessage.value = data.message;

  }
};

// refresh the board on clicking the refresh button

const resetPieces = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/reset', {
      method: 'POST',
    });
    const data = await response.json();
    if (data.status === 'success') {
      pieces.value = data.board_state;
      console.log('Board reset:', pieces.value);
      turn.value = 'White'; // Reset turn to White
      childRef.value?.resetCapturedPieces();
      updateCheckState(data)
    } else {
      console.error('Error resetting board:', data.message);
    }
  } catch (error) {
    console.error('Error resetting board:', error);
  }
};

// Piece promotion code:

const showPromotionModal = ref(false);
const pendingPromotionMove = ref<{
  from: string;
  to: string
} | null>(null);

const isPromotionMove = (piece: Piece, to: string) => {
  if (piece.type !== 'p') return false;

  const rank = to[1];
  return (
    (piece.color === 'white' && rank === '8') ||
    (piece.color === 'black' && rank === '1')
  );
};

const promotePiece = async (piece: 'q' | 'r' | 'b' | 'n') => {
  if (!pendingPromotionMove.value) return;

  const { from, to } = pendingPromotionMove.value;
  showPromotionModal.value = false;
  pendingPromotionMove.value = null;

  const move = `${from}${to}${piece}`

  const response = await fetch('http://127.0.0.1:5000/move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ move }),
  });

  const data = await response.json();

  if (data.status === 'success') {
    pieces.value = data.board_state;
    turn.value = data.turn;
    childRef.value?.fetchCapturedPieces();
    updateCheckState(data)

    // Computer's turn
    if (turn.value === 'Black') {
      setTimeout(async () => {
        await fetchPieces();
        childRef.value?.fetchCapturedPieces();
      }, 1500);
    }
  } else {
    errorMessage.value = data.message;
  }
};

// Check popup

const inCheck = ref(false);
const checkType = ref<'Check' | 'Checkmate'>('Check');

const updateCheckState = (data: MoveResponse) => {
  if (data.check === undefined && data.checkmate === undefined) {
    return; // This will make sure the popup stays open on refresh.
  }
  if (data.checkmate) {
    inCheck.value = true;
    checkType.value = 'Checkmate'
  } else if (data.check) {
    inCheck.value = true;
    checkType.value = 'Check'
  } else {
    inCheck.value = false;
  }
};

// function onPlayerClick(square: Square) {
//   inCheck.value = false;
//   handleSquareClick(square);
// }

onMounted(() => {
  fetchPieces();
});
</script>

<template>
  <InvalidMove v-if="errorMessage" :message="errorMessage" @close="errorMessage = null" />
  <CapturedPieces ref="childRef"/>
  <PomotePieceModal v-if="showPromotionModal" @select="promotePiece" />
  <InCheck :show="inCheck" :message="checkType" />

   <div class="chess-board-container">
     <div v-for="(_, index) in 64" :key="index" class="square" :class="{ dark: isDark(index), selected: selectedSquare === indexToSquare(index) }" @click="onSquareClick(index)">
      <span v-if="pieceAt(index)" class="piece" :class="pieceAt(index)!.color">{{ pieceSymbol(pieceAt(index)!) }}</span>
      <!-- <small class="coord">{{ indexToSquare(index) }}</small> -->
     </div>
   </div>
   <h2>Current Turn: {{ turn }}</h2>
   <button class="refresh-btn" @click="resetPieces">Reset Board</button>
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
.refresh-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 7%;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8);
}
/* .coord {
  position: absolute;
  font-size: 0.6rem;
  color: red;
  bottom: 2px;
  right: 2px;
} */


</style>
