package tictactoe;

import java.util.Random;

public class EasyPlayer extends Player{

    EasyPlayer(Figure symbol, Board board) {
        super("easy", symbol, board);
    }

    EasyPlayer(String name, Figure symbol, Board board) {
        super(name, symbol, board);
    }

    @Override
    void move() {
        while (true)  {
            try {
                board.setFigure(this.getRandomCoordinates(), this.getFigure());
                return;
            } catch (IllegalArgumentException ignored) {
            }
        }
    }

    private Coordinate getRandomCoordinates() {
        Random random = new Random();
        int x = random.nextInt(3);
        int y = random.nextInt(3);
        return new Coordinate(x + 1, y + 1);
    }
}
