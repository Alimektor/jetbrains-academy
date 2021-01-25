package tictactoe;

public abstract class Player {
    protected final String name;
    protected final Figure figure;
    protected final Board board;

    Player(String name, Figure symbol, Board board) {
        this.name = name;
        this.figure = symbol;
        this.board = board;
    }

    Figure getFigure() {
        return this.figure;
    }

    protected String getMessage() {
        return "Making move level \"" + this.name +"\"";
    }

    abstract void move();
}
