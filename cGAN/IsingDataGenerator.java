import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.io.BufferedWriter;
import java.io.FileWriter;


public class IsingDataGenerator {
    private final int N;
    private final double J;
    private final int[][] lattice;
    private final Random random;
    private final List<Double> energySeries;
    private final List<Double> magnetizationSeries;

    public IsingDataGenerator(int N, double J) {
        this.N = N;
        this.J = J;
        this.lattice = new int[N][N];
        this.random = new Random();
        this.energySeries = new ArrayList<>();
        this.magnetizationSeries = new ArrayList<>();

    }

    public void initialiseLattice(double T){
        if (T > 2.2){
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    lattice[i][j] = random.nextBoolean() ? 1 : -1;
                }
            }
        }
        else{
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    lattice[i][j] = 1;
                }
            }
        }
    }

    public double energy() {
        double E = 0.0;
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                E -= J * lattice[i][j] * (lattice[(i + 1) % N][j] + lattice[i][(j + 1) % N] + lattice[(i - 1 + N) % N][j] + lattice[i][(j - 1 + N) % N]);
            }
        }
        return E;
    }

    public double magnetization() {
        double M = 0.0;
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                M += lattice[i][j];
            }
        }
        return M;
    }

    public double monteCarloStep(double T) {

        double finalDeltaE = 0.0;
        for (int k = 0; k < N * N; k++) {
            // Choose a random spin
            int i = random.nextInt(N);
            int j = random.nextInt(N);

            // Calculate the energy difference
            double deltaE = 2.0 * J * lattice[i][j] * (lattice[(i + 1) % N][j] + lattice[i][(j + 1) % N] + lattice[(i - 1 + N) % N][j] + lattice[i][(j - 1 + N) % N]);

            // Metropolis Criterion
            if (deltaE < 0.0 || random.nextDouble() < Math.exp(-deltaE / T)) {
                lattice[i][j] *= -1;
                finalDeltaE += 2*deltaE;
            }
        }
        return finalDeltaE;
    }

    public void simulate(double T, int steps) {
        initialiseLattice(T);
        double E = energy();
        for (int step = 0; step < steps; step++) {
            E += monteCarloStep(T);
            double M = magnetization();
            // System.out.println(step + "\t" + E + "\t" + M);
            energySeries.add(E);
            magnetizationSeries.add(M);
        }
    }


    public void SaveImage(String filename) {
        int size = 600; // image size
        BufferedImage image = new BufferedImage(size, size, BufferedImage.TYPE_INT_RGB);
        Graphics g = image.getGraphics();
        // write image
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (lattice[i][j] == 1) {
                    g.setColor(Color.BLACK);
                } else {
                    g.setColor(Color.WHITE);
                }
                g.fillRect(i * size / N, j * size / N, size / N + 1, size / N + 1);
            }
        }

        g.dispose();

        try {
            ImageIO.write(image, "png", new File(filename));
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void saveSeries(String filename, List<Double> series) {
        try {
            PrintWriter writer = new PrintWriter((filename));
            for (double value : series) {
                writer.println(value);
            }
            writer.close();
        } catch (FileNotFoundException e) {
            System.err.println("Failed to save " + filename);
        }
    }


    public void saveLattice(String fileName, int[][] lattice){

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (int[] row : lattice) {
                for (int element : row) {
                    writer.write(element + ",");
                }
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Failed to save " + e.getMessage());
        }
    }






    public static void main(String[] args) {
        int N = 100;
        double J = 1.0;
        double TMax = 4;
        double TMin = 1.5;
        List<Double> TSeries = new ArrayList<>();
        int steps = 1000;
        int genSize = 15000;
        String tempFile = "./dataset/temperature_record.csv";


        IsingDataGenerator model = new IsingDataGenerator(N, J);

        Random r = new Random();


        for (int l = 0; l < genSize; l++) {
            double T = (r.nextDouble() * (TMax - TMin)) + TMin;
            int L = l + 1;
            TSeries.add(T);
            model.simulate(T, steps);
            String energyFile = "./dataset/energy_data/energy_" + L + ".csv";
            String magnetisationFile = "./dataset/magnetisation_data/magnetisation_" + L + ".csv";
            String latticeFile = "./dataset/lattice_data/lattice_" + L + ".csv";
            String imageFile = "./dataset/image_data/image_" + L + ".png";
            model.SaveImage(imageFile);
            //model.saveSeries(energyFile, model.energySeries);
            //model.saveSeries(magnetisationFile, model.magnetizationSeries);
            model.saveLattice(latticeFile, model.lattice);
            System.out.println(L);
        }

        model.saveSeries(tempFile, TSeries);
    }
}