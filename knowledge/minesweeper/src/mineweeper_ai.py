import itertools
import random
from sentence import *

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge: list[Sentence] = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        
    def nearby_cells_set(self, cell):
        """
        Returns a set of nearby cells excluding cells known to be mines
        """

        # Keep count of nearby mines
        nearby_mines_set = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i,j) not in self.mines and (i,j) not in self.safes: # if the cell is know to be a mine or safe don`t add it to the list of nearby cells
                        nearby_mines_set.add((i,j))

        return nearby_mines_set

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Collect neighbours and adjust the clue count for already-known mines.
        neighbours = set()
        remaining_count = count
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if not (0 <= i < self.height and 0 <= j < self.width):
                    continue
                neighbour = (i, j)
                if neighbour in self.mines:
                    remaining_count -= 1
                elif neighbour not in self.safes:
                    neighbours.add(neighbour)

        if neighbours:
            new_sentence = Sentence(neighbours, remaining_count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        # Keep inferring until nothing new can be learned.
        changed = True
        while changed:
            changed = False

            # First, mark any certain mines or safes.
            safes_to_mark = set()
            mines_to_mark = set()
            for sentence in self.knowledge:
                safes_to_mark |= sentence.known_safes()
                mines_to_mark |= sentence.known_mines()

            for safe in safes_to_mark - self.safes:
                self.mark_safe(safe)
                changed = True
            for mine in mines_to_mark - self.mines:
                self.mark_mine(mine)
                changed = True

            # Remove empty sentences.
            self.knowledge = [s for s in self.knowledge if s.cells]

            # Try to derive new sentences via subset inference.
            inferred = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 is s2:
                        continue
                    if s1.cells.issubset(s2.cells) and s1.count <= s2.count:
                        diff_cells = s2.cells - s1.cells
                        diff_count = s2.count - s1.count
                        if not diff_cells:
                            continue
                        if diff_count < 0 or diff_count > len(diff_cells):
                            continue
                        candidate = Sentence(diff_cells, diff_count)
                        if candidate not in self.knowledge and candidate not in inferred:
                            inferred.append(candidate)

            if inferred:
                self.knowledge.extend(inferred)
                changed = True

            # Deduplicate sentences to keep the knowledge base tidy.
            unique: list[Sentence] = []
            for sentence in self.knowledge:
                if sentence not in unique and sentence.cells:
                    unique.append(sentence)
            if len(unique) != len(self.knowledge):
                self.knowledge = unique
                changed = True



    


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        candidates = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        if not candidates:
            return None
        return random.choice(candidates)
