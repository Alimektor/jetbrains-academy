package converter;

public class NumeralSystemConverter {
    private static NumeralSystemConverter instance;

    private NumeralSystemConverter() {}

    public static NumeralSystemConverter getInstance() {
        if (instance == null) {
            instance = new NumeralSystemConverter();
        }
        return instance;
    }

    String toBinary(int number) {
        return "0b" + Integer.toBinaryString(number);
    }

    String toOctal(int number) {
        return "0" + Integer.toOctalString(number);
    }

    String toHexadecimal(int number) {
        return "0x" + Integer.toHexString(number);
    }

    public String prettyConvert(int number, int radix) {
        if (radix == 2)
            return this.toBinary(number);
        if (radix == 8)
            return this.toOctal(number);
        if (radix == 16)
            return this.toHexadecimal(number);
        return Integer.toString(number, radix);
    }

    public String convert(int number, int radix) {
        if (radix == 1)
            return "1".repeat(number);
        return Integer.toString(number, radix);
    }

    public int parseInt(String number, int radix) {
        if (radix == 1) {
            int count = 0;
            for (int i = 0; i < number.length(); i++) {
                if (number.charAt(i) == '1')
                    count++;
            }
            return count;
        }
        return Integer.parseInt(number, radix);
    }

    public String convert(String sourceNumber, int sourceRadix, int targetRadix) {
        if (this.isFraction(sourceNumber)) {
            return this.convertFraction(sourceNumber, sourceRadix, targetRadix);
        } else {
            return this.convertInteger(sourceNumber, sourceRadix, targetRadix);
        }
    }

    private boolean isFraction(String number) {
        return number.contains(".");
    }

    private String convertInteger(String sourceNumber, int sourceRadix, int targetRadix) {
        int decimalNumber = convertIntegerToDecimal(sourceNumber, sourceRadix);

        return convertIntegerToTargetRadix(decimalNumber, targetRadix);
    }

    private static int convertIntegerToDecimal(String number, int sourceRadix) {
        if (sourceRadix == 1) {
            return number.length();
        } else {
            return Integer.parseInt(number, sourceRadix);
        }
    }

    private static String convertIntegerToTargetRadix(int decimalNumber, int targetRadix) {
        if (targetRadix == 1) {
            return "1".repeat(decimalNumber);
        } else {
            return Integer.toString(decimalNumber, targetRadix);
        }
    }

    private String convertFraction(String sourceNumber, int sourceRadix, int targetRadix) {
        String[] parts = sourceNumber.split("\\.");

        int decimalIntegerPart = convertIntegerToDecimal(parts[0], sourceRadix);
        double decimalFractionalPart = convertFractionalPartToDecimal(parts[1], sourceRadix);
        double decimalFractionalNumber = decimalIntegerPart + decimalFractionalPart;

        return convertFractionToTargetRadix(decimalFractionalNumber, targetRadix);
    }

    private double convertFractionalPartToDecimal(String fractionalPart, int sourceRadix) {
        double result = 0;

        for (int i = 0; i < fractionalPart.length(); i++) {
            if (Character.isDigit(fractionalPart.charAt(i))) {
                result += (fractionalPart.charAt(i) - '0') / Math.pow(sourceRadix, i + 1);
            } else {
                result += (fractionalPart.charAt(i) - 'a' + 10) / Math.pow(sourceRadix, i + 1);
            }
        }

        return result;
    }

    private String convertFractionToTargetRadix(double decimalFractionalNumber, int targetRadix) {
        int integerPart = (int) decimalFractionalNumber;
        double fractionalPart = decimalFractionalNumber - integerPart;
        StringBuilder result = new StringBuilder();

        for (int i = 0; i < 5; i++) {
            int digit = (int) (fractionalPart * targetRadix);
            fractionalPart = fractionalPart * targetRadix - digit;
            result.append(convertIntegerToTargetRadix(digit, targetRadix));
        }

        return convertIntegerToTargetRadix(integerPart, targetRadix) + "." + result;
    }

}
