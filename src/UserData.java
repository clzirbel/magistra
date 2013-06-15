// UserData.java is the class for a collection of word pairs in Magistra
import java.io.*;
import java.util.*;

public class UserData {
    private String Filename;
    private String[] PairData = new String[9999];
    private String[] Indices = new String[9999];
    private int NumPairData;
    private int NumKnown = 0;

    // Constructor - read the specified file, fill in all fields
    public UserData (String Filename) {
	this.Filename = Filename;

    String currentLine = null;
    StringTokenizer st;
    int i = 0;

    BufferedReader in = null;

    try {
       in = new BufferedReader(new FileReader(Filename));
    while( (currentLine = in.readLine()) != null) {
      st = new StringTokenizer(currentLine,"\t\n\r\f");
      Indices[i] = st.nextToken();
      PairData[i] = st.nextToken();
      i++;
    }
    NumPairData = i;
    NumKnown = countNumKnown();
    System.out.println("Read "+Filename);
    System.out.println("Number known is " + NumKnown);
    }
    catch (IOException e) {
	System.out.println("Welcome to Magistra!");
        NumPairData = 0;
    }
  }

    // methods for accessing data in UserData

    public String toString() { return Filename; };
    public String getIndex(int N) { return Indices[N]; };
    public String getPairData(int N) { return PairData[N]; };
    public int getNumPairData() { return NumPairData; };
    public String getFilename() { return Filename; };
    public int getNumKnown() { return NumKnown; };
    
	/**
	 * Loops through PairData to count the number that are officially "known"
	 * 
	 * 
	 */

    public int countNumKnown() {
    	int n = 0;
    	for (int i = 0; i < NumPairData; i++)
    		n += evaluatePairData(PairData[i]);
    	return n;
    }
    
    public static int evaluatePairData(String pairData) {
    	
    	int s = 0;

    	pairData = pairData.replace("#", "");      // just in case it has been practiced the other direction too
    	
    	if (pairData.equals("+"))
    		s = 1;
    	if (pairData.endsWith("++"))
    		s = 1;
    	if (pairData.endsWith("P+"))               // previewed, then right
    		s = 1;
    	
    	return s;
    }
}
