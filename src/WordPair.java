// WordPair.java is the class for each word pair in Magistra
// import java.io.*;
import java.util.*;

public class WordPair extends Object {
   private String[] Word = new String[2];
   private String PartOfSpeech;
   private int Group;
   private String UserData = new String("");
   private int NumTries = 0;
   private float priority = 0;
   private char FirstResult = '?';
   private boolean removed = false;

   public WordPair( String W1, String W2, int G ) {
	   if ((W1.charAt(0) == '"') & (W1.charAt(W1.length()-1)=='"'))
		   W1 = W1.replaceAll("\"", "");
	   if ((W2.charAt(0) == '"') & (W2.charAt(W2.length()-1)=='"'))
		   W2 = W2.replaceAll("\"", "");
	   this.Word[0] = W1;        // remove double quotes
       this.Word[1] = W2;        // remove double quotes
       this.PartOfSpeech = "Unknown";
       this.Group = G;
   }

   public String toString() { return Word[0] + " | " + Word[1]; };
   public String getWord(int L) { return Word[L]; };
   public String getPOS() { return PartOfSpeech; };
   public int getGroup() { return Group; };
   public void setGroup(int n) { Group = n; };
   public void setBaseWord(String newword) {Word[0] = newword;}
   public void setForeignWord(String newword) {Word[1] = newword;}
   public void setRemoved(boolean r) { removed = r; }
   public boolean getRemoved() {return removed;}
   public String getUserData() { return UserData; };
   public void modifyPairData(String ns) { UserData = UserData + ns; };
   public boolean compareStrings(int L, String A) { 
       boolean Correct = false;
       StringTokenizer st;
       Correct = (Word[L].compareTo(A) == 0);
       st = new StringTokenizer(Word[L],";");
       while(st.hasMoreTokens()) {
	   if (A.compareTo(st.nextToken().trim()) == 0)
		   Correct = true;
       }
       return Correct;
   }
   public String portionCorrect(int L, String A) { 
       String p = " --> " + A;
       int numcorrect = 0;                      // number of correct characters, counting from beginning
       StringTokenizer st;
       st = new StringTokenizer(Word[L],";");
       String AA = A + "----------------------------";
       
       while(st.hasMoreTokens()) {
    	   String B = st.nextToken().trim();
    	   String BB = B + "============================";
    	   int nc = 0;
    	   while (AA.charAt(nc) == BB.charAt(nc)) 
    		   nc++;
    	   nc = Math.min(nc, A.length());
    	   nc = Math.min(nc, B.length());

    	   if (nc > numcorrect) {
    		   numcorrect = nc;
    		   p = A.substring(0,nc) + " --> " + A.substring(nc);
    	   }
       }
       return p;
   }

    public boolean containsString(int L, String A) {
		boolean Contains = false;
		Contains = (Word[L].toLowerCase().indexOf(A.toLowerCase()) >= 0);
        return Contains;
    }
   public void registerTry() { NumTries++; };
   public int getNumTries() {return NumTries; };
   public float getPriority() { return priority; };
   public void setPriority(float p) { priority = p; };
   public void setFirstResult(char f) { FirstResult = f; };
   public char getFirstResult() { return FirstResult; };
}
