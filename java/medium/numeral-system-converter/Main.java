package converter;

import java.util.Scanner;

public class Main {
    static Scanner scanner = new Scanner(System.in);
    static NumeralSystemConverter converter = NumeralSystemConverter.getInstance();

    public static void main(String[] args) {
        try {
            int sourceRadix = Integer.parseInt(scanner.nextLine());
            String sourceNumber = scanner.nextLine();
            int targetRadix = Integer.parseInt(scanner.nextLine());

            if (sourceRadix > 36)
                throw new IllegalArgumentException("Source radix must be less than 36");

            if (sourceRadix < 1)
                throw new IllegalArgumentException("Source radix must be more than 1");

            if (targetRadix > 36)
                throw new IllegalArgumentException("Target radix must be less than 36");

            if (targetRadix < 1)
                throw new IllegalArgumentException("Target radix must be more than 1");

            System.out.println(converter.convert(sourceNumber, sourceRadix, targetRadix));
        } catch (Exception exception) {
            System.out.println("Some error occurred.");
        }
    }
}
