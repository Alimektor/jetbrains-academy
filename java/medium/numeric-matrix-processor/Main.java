package processor;

import java.util.Scanner;

public class Main {
    private static final Scanner scanner = new Scanner(System.in);
    private static MenuChoice menuChoice;
    private static TransposeChoice transposeChoice;

    public static void _main(String[] args) {
        Matrix matrix = createMatrix("");
        System.out.println(matrix.getDeterminant());
    }

    public static void main(String[] args) {
        do {
            printMenu();
            setMenuChoice();
            try {
                switch (menuChoice) {
                    case ADDING:
                        add();
                        break;
                    case MULTIPLY_BY_CONSTANT:
                        multiply_by_constant();
                        break;
                    case MULTIPLY_MATRICES:
                        multiply_matrices();
                        break;
                    case TRANSPOSED:
                        transposed();
                        break;
                    case INVERSE:
                        inverse();
                        break;
                    case DETERMINANT:
                        determinant();
                        break;
                }
            } catch (IllegalArgumentException ial) {
                System.out.println(ial.getMessage());
            }
        } while (menuChoice != MenuChoice.EXIT);
    }

    private static void getResultMessage() {
        System.out.println("The result is:");
    }

    private static void add() {
        Matrix matrix1 = createMatrix("first ");
        Matrix matrix2 = createMatrix("second ");
        getResultMessage();
        System.out.println(matrix1.add(matrix2));
    }

    private static void multiply_by_constant() {
        Matrix matrix1 = createMatrix("");
        System.out.println("Enter constant: ");
        int constant = scanner.nextInt();
        getResultMessage();
        System.out.println(matrix1.multiply(constant));
    }

    private static void multiply_matrices() {
        Matrix matrix1 = createMatrix("first ");
        Matrix matrix2 = createMatrix("second ");
        getResultMessage();
        System.out.println(matrix1.multiply(matrix2));
    }

    private static void transposed() {
        printTransposedMenu();
        setTransposeChoice();
        Matrix matrix = createMatrix("");
        switch (transposeChoice) {
            case MAIN:
                System.out.println(matrix.getMainTransposed());
                break;
            case SIDE:
                System.out.println(matrix.getSideTransposed());
                break;
            case VERTICAL:
                System.out.println(matrix.getVerticalTransposed());
                break;
            case HORIZONTAL:
                System.out.println(matrix.getHorizontalTransposed());
                break;
        }
    }

    private static Matrix createMatrix(String which) {
        System.out.printf("Enter size of %smatrix:\n", which);
        int row = scanner.nextInt();
        int column = scanner.nextInt();
        Matrix matrix = new Matrix(row, column);
        System.out.printf("Enter %smatrix:\n", which);
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < column; j++) {
                matrix.setItem(i, j, scanner.nextDouble());
            }
        }
        return matrix;
    }

    private static void printMenu() {
        System.out.println("1. Add matrices");
        System.out.println("2. Multiply matrix by a constant");
        System.out.println("3. Multiply matrices");
        System.out.println("4. Transpose matrix");
        System.out.println("5. Calculate a determinant");
        System.out.println("6. Inverse matrix");
        System.out.println("0. Exit");
    }

    private static void printTransposedMenu() {
        System.out.println("1. Main diagonal");
        System.out.println("2. Side diagonal");
        System.out.println("3. Vertical line");
        System.out.println("4. Horizontal line");
    }

    private static void setMenuChoice() {
        System.out.println("Your choice:");
        menuChoice = MenuChoice.values()[scanner.nextInt()];
    }

    private static void setTransposeChoice() {
        System.out.println("Your choice:");
        transposeChoice = TransposeChoice.values()[scanner.nextInt()];
    }

    private static void inverse() {
        Matrix matrix = createMatrix("");
        getResultMessage();
        System.out.println(matrix.getInverse());
    }

    private static void determinant() {
        Matrix matrix = createMatrix("");
        getResultMessage();
        System.out.println(matrix.getDeterminant());
    }
}
