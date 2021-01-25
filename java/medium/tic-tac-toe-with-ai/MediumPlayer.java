package tictactoe;

public class MediumPlayer extends EasyPlayer {
    private Coordinate playerMove;

    MediumPlayer(Figure symbol, Board board) {
        super("medium", symbol, board);
    }

    MediumPlayer(String name, Figure symbol, Board board) {
        super(name, symbol, board);
    }

    @Override
    void move() {
        while (true)  {
            try {
                if (this.canWin(this.figure)) {
                    this.board.setFigure(this.playerMove, this.getFigure());
                    return;
                }
                Figure opponentFigure = Figure.O_SYMBOL;
                if (this.figure == Figure.O_SYMBOL) {
                    opponentFigure = Figure.X_SYMBOL;
                }

                if (this.canWin(opponentFigure)) {
                    this.board.setFigure(this.playerMove, this.getFigure());
                    return;
                }
                super.move();
                break;
            } catch (IllegalArgumentException ignored) {
            }
        }
    }

    private boolean canWin(Figure figure) {

        for (int row = 1; row <= this.board.getLength(); row++) {
            if (this.board.getCountOnRow(figure, row) == 2 && this.board.getCountOnRow(Figure.EMPTY, row) == 1) {
                this.playerMove = this.board.getEmptyOnlyRow(row);
                return true;
            }
        }

        for (int column = 1; column <= this.board.getLength(); column++) {
            if (this.board.getCountOnColumn(figure, column) == 2 && this.board.getCountOnColumn(Figure.EMPTY, column) == 1) {
                this.playerMove = this.board.getEmptyOnlyColumn(column);
                return true;
            }
        }

        if (this.board.getCountOnMainDiagonal(figure) == 2 && this.board.getCountOnMainDiagonal(Figure.EMPTY) == 1) {
            this.playerMove = this.board.getEmptyOnlyMainDiagonal();
            return true;
        }

        if (this.board.getCountOnSideDiagonal(figure) == 2 && this.board.getCountOnSideDiagonal(Figure.EMPTY) == 1) {
            this.playerMove = this.board.getEmptyOnlySideDiagonal();
            return true;
        }

        return false;
    }
}
