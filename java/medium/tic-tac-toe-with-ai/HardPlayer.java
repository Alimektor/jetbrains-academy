package tictactoe;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class HardPlayer extends MediumPlayer {

    HardPlayer(Figure symbol, Board board) {
        super("hard", symbol, board);
    }

    HardPlayer(String name, Figure symbol, Board board) {
        super(name, symbol, board);
    }

    @Override
    void move() {
        try {
            Board copyBoard = new Board(this.board);
            ArrayList<Integer> scoresOfMoves = new ArrayList<>();
            Coordinate[] availableMoves = board.freeMoves();

            for (Coordinate cell : availableMoves) {
                scoresOfMoves.add(this.getScore(copyBoard, true, cell));
            }

            int bestMoveIndex = scoresOfMoves.indexOf(Collections.max(scoresOfMoves));
            Coordinate bestMove = availableMoves[bestMoveIndex];
            this.board.setFigure(bestMove, this.getFigure());
        } catch (IllegalArgumentException illegalArgumentException) {
            System.out.println(illegalArgumentException.getMessage());
        }
    }

    private int getScore(Board board, boolean isPlayer, Coordinate cell) {
        Figure symbol;
        if (isPlayer)
            symbol = this.getFigure() == Figure.X_SYMBOL ? Figure.X_SYMBOL : Figure.O_SYMBOL;
        else
            symbol = this.getFigure() == Figure.X_SYMBOL ? Figure.O_SYMBOL : Figure.X_SYMBOL;
        board.setCell(cell, symbol);
        int score = this.minimax(board, isPlayer);
        board.setCell(cell, Figure.EMPTY);
        return score;
    }

    private int minimax(Board board, boolean isPlayer) {
        State check = board.check();
        switch (check) {
            case Draw:
                return 0;
            case xWins:
                if (this.getFigure() == Figure.X_SYMBOL)
                    return 10;
                else
                    return -10;
            case oWins:
                if (this.getFigure() == Figure.O_SYMBOL)
                    return 10;
                else
                    return -10;
        }

        Coordinate[] availableMoves = board.freeMoves();
        ArrayList<Integer> scoresOfMoves = new ArrayList<>();


        for (Coordinate coordinate : availableMoves) {
            int score;
            if (isPlayer) {
                score = this.getScore(board, false, coordinate);
                if (score == -10)
                    return score;
            } else {
                score = this.getScore(board, true, coordinate);
                if (score == 10)
                    return score;
            }
            scoresOfMoves.add(score);
        }

        if (isPlayer)
            return Collections.min(scoresOfMoves);
        return Collections.max(scoresOfMoves);
    }
}
