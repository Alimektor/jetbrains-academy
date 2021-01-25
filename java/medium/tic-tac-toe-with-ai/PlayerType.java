package tictactoe;

public enum PlayerType {
    USER("user"),
    EASY("easy"),
    MEDIUM("medium"),
    HARD("hard");

    private final String type;

    PlayerType(String playerType) {
        this.type = playerType;
    }

    public String getType() {
        return this.type;
    }
}
