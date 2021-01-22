package processor;

public enum TransposeChoice {
    NONE(0),
    MAIN(1),
    SIDE(2),
    VERTICAL(3),
    HORIZONTAL(4);

    public final int choice;

    TransposeChoice(final int choice) {
        this.choice = choice;
    }

    public int getChoice() {
        return choice;
    }
}
