package tictactoe;

public enum MenuChoice {
    START("start"),
    EXIT("exit");

    private final String choice;

    MenuChoice(String choice) {
        this.choice = choice;
    }

    public String getChoice() {
        return choice;
    }

    public static MenuChoice setChoice(String choice) {
        for (MenuChoice value : MenuChoice.values()) {
            if (value.getChoice().equals(choice))
                return value;
        }
        throw new IllegalArgumentException("Bad parameters");
    }
}
