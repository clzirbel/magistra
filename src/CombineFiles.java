//CombineFiles.java - read and tokenize the file
import java.io.*;
import java.util.*;

class CombineFiles {
  public static void main(String[] args)
        throws IOException
  {
    String currentString = null;
    String fileName = "all";
    String[] files = new String[100];
    StringTokenizer st;
    int i = 1;

    files[1] = "400";
    files[2] = "500";
    files[3] = "600";
    files[4] = "700";
    files[5] = "800";
    files[6] = "900";
    files[7] = "1000";
    files[8] = "1100";
    files[9] = "1200";
    files[10] = "alex1";
    files[11] = "arruga";
    files[12] = "gringo";
    files[13] = "irrpres";
    files[14] = "perio1";
    files[15] = "sentence";
    files[16] = "simple1";
    files[17] = "simple2";
    files[18] = "verbs";

    PrintWriter out = new PrintWriter(new FileWriter("Spanish2.txt"));

    int f;
    for (f = 1; f <= 18; f++) {
      System.out.println(f);
      BufferedReader in = new BufferedReader(new FileReader(files[f] + ".spa"));
      currentString = in.readLine();
      while( (currentString = in.readLine()) != null)  {
	  if (currentString.length() > 2) {
        System.out.println(files[f] + "  " + currentString);
        st = new StringTokenizer(currentString,"\"\t\n\r\f");
        out.print(i + "\t");
        out.print(st.nextToken() + "\t");
        st.nextToken();
        out.print(st.nextToken() + "\t");
        out.print(files[f] + "\n");
        i++;
}
      }

      // also write out the indices to a file called files[f] + ".list"

    }
    out.close();
  }
}
