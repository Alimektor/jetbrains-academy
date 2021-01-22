package processor;

enum MenuChoice {
    EXIT(0),
    ADDING(1),
    MULTIPLY_BY_CONSTANT(2),
    MULTIPLY_MATRICES(3),
    TRANSPOSED(4),
    DETERMINANT(5),
    INVERSE(6);

    public final int choice;

    MenuChoice(final int choice) {
        this.choice = choice;
    }

    public int getChoice() {
        return choice;
    }
}
