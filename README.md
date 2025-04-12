Code usage: python TicTacToe(Server/Client).py <port_number>. Example 
usage: python3 TicTacToeServer 6000. python3 TicTacToeClient 6000. 
python3 TicTacToeClient 6000.

Three terminals needs to be opened. I tried the code in cmd terminals,
Linux terminals, and PyCharm and VsCode terminals. First TicTacToeServer 
needs to be initialized. Then, two TicTacToeClientcode needs to be initialized. 
First one (init. order) is assigned to Player 0 and symbol 'X'. Second one is 
assiged to Player 1 and 'O'. 

Playing the game: To place the assigned symbol, player needs to type where he/she
wants in order (row, column). For the standard Tic Tac Toe table we have three rows
and three columns. Indexing starts from 0 until 2 for the three rows and colums. For 
example, if the player want to place the symbol to 1st row 2nd column, he/she needs 
to type "0,1". for the center "1,1". (Note: the row, column rep. is without paranthases)  

Warning messages is displayed when incorrect moves are played. Incorrect moves consists 
of trying to play to an occupied space, table space that is out of board, and when the turn 
is not the player's turn. Also when the player tries play using incorrect representation, 
i.e, reprenstation fromat is different from row, col. such as a random text, the server gives 
the message "Invalid move format! Please enter row and column numbers separated by a comma" 
to the client.

Also the game has a chat function. If we type "chat" (case sensitive, hence, small letters)
as the input then the next characters typed in the same line is treated as chat message and
delivered to the other client.

When the game ends in win or draw, the result is displayed in the client and server terminals.