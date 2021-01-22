package processor;

public class Matrix {
    private double[][] matrix;

    public Matrix(int row, int column) {
        this.matrix = new double[row][column];
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        for (double[] row : this.matrix) {
            for (double column : row) {
                result.append(column).append(' ');
            }
            result.append('\n');
        }
        return result.toString();
    }

    public void setItem(int row, int column, double value) {
        this.matrix[row][column] = value;
    }

    private int getRows() {
        return this.matrix.length;
    }

    private int getColumns() {
        if (this.matrix.length > 0)
            return this.matrix[0].length;
        return 0;
    }

    private double getItem(int row, int column) {
        return this.matrix[row][column];
    }

    public Matrix add(Matrix other) {
        try {
            if (this.getRows() != other.getRows() || this.getColumns() != other.getColumns())
                throw new IllegalArgumentException("ERROR");
            Matrix result = new Matrix(this.getRows(), this.getColumns());
            for (int row = 0; row < this.getRows(); row++) {
                for (int column = 0; column < this.getColumns(); column++) {
                    result.setItem(row, column, this.getItem(row, column) + other.getItem(row, column));
                }
            }
            return result;
        } catch (Exception exception) {
            System.out.println(exception.getMessage());
        }
        return new Matrix(0, 0);
    }

    public Matrix multiply(int constant) {
        Matrix result = new Matrix(this.getRows(), this.getColumns());
        for (int row = 0; row < this.getRows(); row++) {
            for (int column = 0; column < this.getColumns(); column++) {
                result.setItem(row, column, this.getItem(row, column) * constant);
            }
        }
        return result;
    }

    public Matrix multiply(Matrix other) throws IllegalArgumentException {
        if (this.getColumns() != other.getRows()) {
            throw new IllegalArgumentException("The operation cannot be performed.");
        }
        Matrix result = new Matrix(this.getRows(), other.getColumns());
        for (int row = 0; row < this.getRows(); row++) {
            for (int column = 0; column < other.getColumns(); column++) {
                double dot = 0;
                for (int cell = 0; cell < this.getColumns(); cell++) {
                    dot += this.getItem(row, cell) * other.getItem(cell, column);
                }
                result.setItem(row, column, dot);
            }
        }
        return result;
    }

    public Matrix getMainTransposed() {
        Matrix result = new Matrix(this.getColumns(), this.getRows());
        for (int row = 0; row < this.getRows(); row++) {
            for (int column = 0; column < this.getColumns(); column++) {
                result.setItem(column, row, this.getItem(row, column));
            }
        }
        return result;
    }

    public Matrix getSideTransposed() {
        return this.getMainTransposed().getHorizontalTransposed().getVerticalTransposed();
    }

    public Matrix getVerticalTransposed() {
        Matrix result = new Matrix(this.getColumns(), this.getRows());
        for (int row = 0; row < this.getRows(); row++) {
            for (int column = 0, columnResult = this.getColumns() - 1; column < this.getColumns(); column++, columnResult--) {
                result.setItem(row, column, this.getItem(row, columnResult));
            }
        }
        return result;
    }

    public Matrix getHorizontalTransposed() {
        Matrix result = new Matrix(this.getColumns(), this.getRows());
        for (int row = 0; row < this.getRows(); row++) {
            result.matrix[result.getRows() - row - 1] = this.matrix[row];
        }
        return result;
    }

    public double getDeterminant() {
        Matrix copiedMatrix = this.getCopied();
        double[] temp = new double[copiedMatrix.getRows()];
        double total = 1;
        double determinant = 1;
        int n = copiedMatrix.getRows();
        for (int i = 0; i < copiedMatrix.getRows(); i++) {
            int index = i;
            while (index < copiedMatrix.getRows() && copiedMatrix.getItem(index, i) == 0) {
                index += 1;
            }
            if (index == copiedMatrix.getRows())
                continue;
            if (index != i) {
                for (int j = 0; j < n; j++) {
                    double swap = copiedMatrix.getItem(index, j);
                    copiedMatrix.setItem(index, i, copiedMatrix.getItem(i, j));
                    copiedMatrix.setItem(i, j, swap);
                }
                determinant *= (int) Math.pow(-1, index - i);
            }
            for (int j = 0; j < n; j++) {
                temp[j] = copiedMatrix.getItem(i, j);
            }

            for (int j = i + 1; j < n; j++) {
                double num1 = temp[i];
                double num2 = copiedMatrix.getItem(j, i);
                for (int k = 0; k < n; k++) {
                    double value = (num1 * copiedMatrix.getItem(j, k)) - (num2 * temp[k]);
                    copiedMatrix.setItem(j, k, value);
                }
                total *= num1;
            }
        }

        for (int i = 0; i < n; i++) {
            determinant *= copiedMatrix.getItem(i, i);
        }

        return (determinant / total);
    }

    public Matrix getInverse() {
        if (!this.checkSquareness() || !this.checkNotSingular())
            throw new IllegalArgumentException("This matrix doesn't have an inverse.\n");

        double determinant = this.getDeterminant();

        Matrix cofactors = this.getCopied();

        if (cofactors.getRows() == 2 && cofactors.getColumns() == 2) {
            cofactors.setItem(0 , 0, this.getItem(1, 1) / determinant);
            cofactors.setItem(0 , 1, -1 * this.getItem(0, 1) / determinant);
            cofactors.setItem(1 , 0, -1 * this.getItem(1, 0) / determinant);
            cofactors.setItem(1 , 1, this.getItem(0, 0) / determinant);
            return cofactors;
        }

        for (int row = 0; row < cofactors.getRows(); row++) {
            for (int column = 0; column < cofactors.getColumns(); column++) {
                Matrix minor = this.getMinor(row, column);
                cofactors.setItem(row, column, Math.pow((-1), (row + column)) * minor.getDeterminant());
            }
        }

        cofactors = cofactors.getMainTransposed();

        for (int row = 0; row < cofactors.getRows(); row++) {
            for (int column = 0; column < cofactors.getColumns(); column++) {
                cofactors.setItem(row, column, (cofactors.getItem(row, column) / determinant));
            }
        }

        return cofactors;
    }

    private Matrix getCopied() {
        Matrix matrix = new Matrix(this.getRows(), this.getColumns());
        for (int row = 0; row < this.getRows(); row++) {
            for (int column = 0; column < this.getColumns(); column++) {
                matrix.setItem(row, column, this.getItem(row, column));
            }
        }
        return matrix;
    }

    private boolean checkNotSingular() {
        return this.getDeterminant() != 0;
    }

    private boolean checkSquareness() {
         return this.getRows() == this.getColumns();
    }

    private double[] getRow(int index) {
        return this.matrix[index];
    }

    public void deleteRow(int index) {
        double[][] temp = new double[this.getRows() - 1][this.getColumns()];
        for (int row = 0, i = 0; row < this.getRows(); row++) {
            if (!(index == row)) {
                temp[i] = this.getRow(row);
                i++;
            }
        }
        this.matrix = temp;
    }

    public void deleteColumn(int index) {
        double[][] temp = new double[this.getRows()][this.getColumns() - 1];
        for (int row = 0; row < this.getRows(); row++) {
            for (int column = 0, j = 0; column < this.getColumns(); column++) {
                if (!(index == column)) {
                    temp[row][j] = this.getItem(row, column);
                    j++;
                }
            }
        }
        this.matrix = temp;
    }

    private Matrix getMinor(int row, int column) {
        Matrix matrix = this.getCopied();
        matrix.deleteRow(row);
        matrix.deleteColumn(column);
        return matrix;
    }
}
