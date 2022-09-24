# Flipping-Board-Game-AI
A Board game with two players. You can flip the opponent's pieces when you new move surrounds opponent's pieces in any directions. Implemented with algorithms like Minimax, Alpha-beta Pruning, etc.

To Run the program, you can either run two separate agents against each other using: 
          python3 bidding gui.py -d N -a <agent1> -b <agent2>
or you can run one agent against an interactive user:
          python3 bidding gui.py -d N -a <agent1>

In both cases, N denotes the board size. Optionally, you can also specify three flags:
• -l <limit>, where <limit> is an integer representing the depth limit (see §Your Tasks - Depth Limiting)
• -c, which enables caching (see §Your Tasks - Caching)
• -o which enables optimal node ordering for α{β-pruning (see §Your Tasks - Optimizing the Node Order for α{β-Pruning)
