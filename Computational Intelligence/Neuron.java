//Matrix class
//Manan Isak
//02/19/2022

public class Neuron {
	int numOfIn;
	double[] inputs;
	double[] weights;
	double threshold;
	double x; // Sum of inputs * weights
	double y; // Activation value
	double error;

	double[][] correctIn = {{0,1,1,1,1},
                      		{1,0,1,1,1},
                     		{1,1,0,1,1},
                     	 	{1,1,1,0,1},
                      		{1,1,1,1,0},
                      		{1,1,1,1,1},
                      		{0,0,0,0,0},
                      		{1,0,0,0,0},
                      		{0,1,0,0,0},
                      		{0,0,1,0,0},
                      		{0,0,0,1,0},
                      		{0,0,0,0,1},
                     		{1,0,0,0,1},
                      		{0,1,0,0,1},
                      		{0,0,1,1,1},
                      		{1,0,1,1,0}};

	public Neuron(int parNumOfIn) {
		numOfIn = parNumOfIn;
		inputs = new double[numOfIn];

		for (int i = 0; i < numOfIn; i++) {
			weights[0] = Math.random();
		}
	}

	public void addInput(String input) {	// For inputting the 5-bit binary number e.g. 00110
		char[] inCharArray = input.toCharArray(); // Assume input is always integer
		for (int i = 0; i < numOfIn; i++) {
			inputs[i] = Float.parseFloat(Character.toString(inCharArray[i]));
		}
	}

	public void sumIn() {
		x = 0;
		for (int i = 0; i < numOfIn; i++) {
			x = x + (inputs[i] * weights[i]);
		}
		y = x - threshold;
	}

	public void sigmoid() {
		//this.data[i][j] = 1/(1+Math.exp(-this.data[i][j]));
    }
}