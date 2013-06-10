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
   public void setGroup(int n) {
   	Group = n;
   }
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
    public boolean containsString(int L, String A) {
	boolean Contains = false;
	Contains = (Word[L].indexOf(A) >= 0);
        return Contains;
    }
   public void registerTry() { NumTries++; };
   public int getNumTries() {return NumTries; };
   public float getPriority() { return priority; };
   public void setPriority(float p) { priority = p; };
   public void setFirstResult(char f) { FirstResult = f; };
   public char getFirstResult() { return FirstResult; };
}
