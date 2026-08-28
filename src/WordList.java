// WordList.java is the class for a collection of word pairs in Magistra
import java.io.*;
import java.util.*;


public class WordList {
    private String Filename;
    private String[] Language = new String[2];
    private Hashtable PairTable;
    private String[] Indices = new String[9999];
    private int[] Order;
    private int numPairs;
    private String[] Selected;
    private String UserDataFilename;
    private int numKnown = 0;

    // Constructor - read the specified file, fill in all fields
    public WordList (String Filename) {
		this.Filename = Filename;

		this.PairTable = new Hashtable();

	    String currentLine = null;
	    StringTokenizer st;
	    int i = 0;

	    BufferedReader in = null;

	    try {
	       in = new BufferedReader(new FileReader(Filename));
	    }
	    catch (IOException e) {
		System.out.println("Could not open " + Filename);
		System.out.println(e);
	    }

	    try {
	    currentLine = in.readLine();
	    st = new StringTokenizer(currentLine,"\t\n\r\f");

	    // Language names must come first
	    Language[0] = st.nextToken();
	    Language[1] = st.nextToken();

	    while( (currentLine = in.readLine()) != null) {
	      st = new StringTokenizer(currentLine,"\t\n\r\f");
	      Indices[i] = st.nextToken();

	      // this would be where we could read names for the groups in the file

	      try {
	      WordPair newpair = new WordPair(st.nextToken(),st.nextToken(),Integer.parseInt(st.nextToken()));
	      Object val = PairTable.put( Indices[i], newpair );
	      i++;
	      }
		catch (NoSuchElementException e) {
			System.out.println("Trouble with " + currentLine);
			System.out.println(e);
		}

	    }
	    numPairs = i;
	    }
	    catch (IOException e) {
		System.out.println("WordList: Something went wrong when reading the word file");
		System.out.println(e);
	    }
    }

    // method for incorporating user data into the word list

    public void incorporateUserData (UserData UD) {
	int NumPairData = UD.getNumPairData();
	UserDataFilename = UD.getFilename();
    numKnown = UD.getNumKnown();

    for (int i=0; i < NumPairData; i++) {
	    WordPair WP;
	    try{
              WP = this.getPair(UD.getIndex(i));
              WP.modifyPairData(UD.getPairData(i));
              this.putPair(UD.getIndex(i), WP);
	    }
	    catch(NullPointerException e) {
	    }
	}
    }


	// method for setting priorities for the word list
	public void setPriorities(int PriorityType) {

		double priority = 0;
		double r;

		for (int i=0; i < numPairs; i++) {
			WordPair WP = this.getPair(Indices[i]);
			String ud = WP.getUserData();
			int g = WP.getGroup();

			if      (ud.endsWith("+++++")) priority = (double)-0.3;
			else if (ud.endsWith("#####")) priority = (double)-0.3;
			else if (ud.endsWith("++++"))  priority = (double)-0.2;
			else if (ud.endsWith("####"))  priority = (double)-0.2;
			else if (ud.endsWith("+++"))   priority = (double)-0.1;
			else if (ud.endsWith("###"))   priority = (double)-0.1;
			else if (ud.endsWith("++"))    priority = (double)0.0;
			else if (ud.endsWith("##"))    priority = (double)0.0;
			else if (ud.endsWith("+"))     priority = (double)0.1;    // got right the last time
			else if (ud.endsWith("#"))     priority = (double)0.1;    // got right the last time
			else if (ud.endsWith("="))     priority = (double)0.3;    // most recently gotten wrong
			else if (ud.endsWith("-"))     priority = (double)0.3;    // most recently gotten wrong
			else if (ud.endsWith("P"))     priority = (double)0.3;    // has been presented but not practiced
			else if (ud.endsWith("f"))     priority = (double)-1000;  // skip forever
			else                           priority = (double)0.2;

	//        System.out.println(ud + " " + priority);

			// give priority to the current group, g
			// give higher priority to words that have been missed recently
			// how to make it skip words in a group that are already known, and go on to the next group?

			if (PriorityType > 0) {                               // work on all pairs in group g
				priority = priority + 1000 - ((g-PriorityType+1000) % 1000);
			}
			else if (PriorityType < 0) {
				if (priority > 0)                                 // work on group g, omit all ++ pairs
					priority = priority + 1000 - ((g+PriorityType+1000) % 1000);
			}
			else if (PriorityType == 0) {                         // work on words that are known
				if (priority > 0)
					priority = priority - 1;
			}


			r = (double)Math.random()-(double)0.5;

			priority = priority + r*r;            // randomize a little
			WP.setPriority(priority);
		}
	}

	// method for setting priorities for the word list
	// new in 2025, looking to invent more options
	public void setPriorities2025(int startingGroup, int repeatPercentage) {

		double practiceProbability = repeatPercentage / 100.0f;  // 25 becomes 0.25

		int priority = 0;  // numerical code according to user data and correctness
		double pp = 0;    // probability that we practice the current word pair
		double groupScore = 0;  // contribution to the score from the group the pair is in
		double score = 0;   // value we return to sort on, practice from largest score to smallest

		// loop over pairs and user data to determine the priority for each word pair
		for (int i=0; i < numPairs; i++) {
			WordPair WP = this.getPair(Indices[i]);
			String ud = WP.getUserData();
			int g = WP.getGroup();  // every pair belongs to just one group ... or make it more than one?

			if      (ud.endsWith("+++++")) priority = -3;   // low priority
			else if (ud.endsWith("#####")) priority = -3;
			else if (ud.endsWith("++++"))  priority = -2;
			else if (ud.endsWith("####"))  priority = -2;
			else if (ud.endsWith("+++"))   priority = -1;
			else if (ud.endsWith("###"))   priority = -1;
			else if (ud.endsWith("++"))    priority = 0;
			else if (ud.endsWith("##"))    priority = 0;
			else if (ud.endsWith("+"))     priority = 1;    // got right the last time
			else if (ud.endsWith("#"))     priority = 1;    // got right the last time
			else if (ud.endsWith("="))     priority = 3;    // most recently gotten wrong
			else if (ud.endsWith("-"))     priority = 3;    // most recently gotten wrong
			else if (ud.endsWith("P"))     priority = 3;    // has been presented but not practiced
			else if (ud.endsWith("f"))     priority = -1000;  // skip forever, do not practice
			else                           priority = 3;    // not seen before, definitely practice

			// System.out.println(ud + " " + priority);

			if (priority == 3) {
				pp = 1;                       // probability 1 of being practiced
			} else if (priority == 2) {
				pp = practiceProbability;      // user-set probability of being practiced
			} else if (priority == 1) {
				pp = practiceProbability;
			} else if (priority == 0) {
				pp = practiceProbability/2;  // half the user-set probability
			} else if (priority == -1) {
				pp = practiceProbability/4;  // lower, the more times it has been gotten right
			} else if (priority == -2) {
				pp = practiceProbability/8;
			} else if (priority == -3) {
				pp = practiceProbability/16;
			}

			// give highest priority when g = startingGroup
			// somewhat lower priority when g = startingGroup + 1
			// much lower priority when g < startingGroup
			if (g >= startingGroup) {
				// when g == startingGroup, it gets 1000 here
				// when g == startingGroup + 1, it gets 990 here, and so on
				groupScore = 1000 - (g - startingGroup);
			} else if (g < startingGroup) {
				groupScore = 20;
			}

			if (Math.random() < pp) {
				score = groupScore + Math.random();  // randomize within this group
			} else {
				score = Math.random();
			}

			System.out.printf("%4d %20s %10.2f %10.2f %s%n", g, ud, groupScore, score, WP);

			WP.setPriority(score);
		}

		System.out.println("startingGroup: " + startingGroup);
		System.out.println("practiceProbability: " + practiceProbability);
	}

	// method for identifying the selected pairs

    public void setSelected(String[] Selected, int numSelected) {
	String[] temp = new String[numSelected];
	for (int i=0; i<numSelected; i++) {
	    temp[i] = Selected[i];
	}
	this.Selected = temp;
    }

    // method for setting the ordering priority

    public void setOrder(int numSelected) {
	double[] Priority = new double[numSelected];

	for (int i=0; i < numSelected; i++) {
	    Priority[i] = -getPair(Selected[i]).getPriority();
	}
	Order = MyArrays.shellSort(Priority,0,numSelected);
    }

    // method for using the order from the file

    public void setOriginalOrder(int numSelected) {
	double[] Priority = new double[numSelected];

	for (int i=0; i < numSelected; i++) {
	    Priority[i] = i;
	}
	Order = MyArrays.shellSort(Priority,0,numSelected);
    }

    // method for writing user data after practicing

    public void writeUserData() {
	try{
    PrintWriter out = new PrintWriter(new FileWriter(UserDataFilename));
    for (int i=0; i < numPairs; i++) {
    	WordPair WP = this.getPair(Indices[i]);
    	if ((WP.getUserData().length() > 0) || (WP.getFirstResult() != '?')) {
    		out.print(Indices[i] + "\t");
        if (WP.getUserData().length() > 0)    // write previous PairData
        	out.print(WP.getUserData());
        if (WP.getFirstResult() != '?')       // write FirstResult from this attempt at the end
        	out.print(WP.getFirstResult());
        out.print("\n");
	}
    }
    out.close();
	}
	catch (IOException e) {
	    System.out.println("Trouble writing user data file\n");
	}
    }

    // method for writing word list

    public void writeWordList() {
	try{
    PrintWriter out = new PrintWriter(new FileWriter(Filename));
    out.print(Language[0]+"\t"+Language[1]+"\n");
    for (int i=0; i < numPairs; i++) {
        	WordPair WP = this.getPair(Indices[i]);
        	if (WP.getRemoved() == false) {
	        	out.print(Indices[i] + "\t");
	            out.print(WP.getWord(0)+"\t");
	            out.print(WP.getWord(1)+"\t");
	            out.print(WP.getGroup()+"\n");
        	}
        	}
    out.close();
	}
	catch (IOException e) {
	    System.out.println("Trouble writing word list\n");
	}
    }

    // methods for accessing data in WordList

    public String toString() { return Language[0] + " | " + Language[1]; };
    public WordPair getPair(String Index) { return  (WordPair)PairTable.get(Index); };
    public WordPair getSelectedPair(int n) {
        return  (WordPair)PairTable.get( Selected[Order[n]] ); };
    public WordPair getPairByNumber(int n) {
        return  (WordPair)PairTable.get( Indices[n] ); };
    public void putPair(String Index, WordPair np) {
      PairTable.put(Index, np);     };
    public void removePair(String Index) {
        WordPair WP = getPair(Index);
        WP.setRemoved(true);
	}
    public void removePair(int number) {
    	WordPair WP = getPairByNumber(number);
        WP.setRemoved(true);
	}
    public void setIndex(int n) {
      Indices[n] = "Removed";
    }
    public void addPair(String Index, WordPair np) {
      PairTable.put(Index, np);
      Indices[numPairs] = Index;
      numPairs++;
    };
    public String getFilename() { return Filename; };
    public String[] getAllIndices() { return Indices; };
    public String getLanguage(int L) { return Language[L]; };
    public int getNumPairs() { return numPairs; };
    public int getNumToPractice() { return Order.length; };
    public void changeNumKnown(int C) { numKnown += C; };
    public int getNumKnown() { return numKnown; };
    public String getIndex(int n) {
    	return Indices[n];
    }
    public int getMaxIndex() {
	int m = 0;
        for (int i=0; i < numPairs; i++) {
          int n = Integer.parseInt(Indices[i].trim());
          if (n > m) {
	      m = n;
	  }
	}
        return m;
    }

    public void revisitLater(int n, int L) {
    	int[] NewOrder = new int[Order.length+1];
    	int M;
    	M = (int) (n+Math.round(L - 1 + 4*Math.random()));                                     // new position for this item
    	                                             // later, make this random with mean L
    	if (M > Order.length)
    		M = Order.length;
    	for (int i=0; i < M; i++) {
    		NewOrder[i] = Order[i];
    	}
    	NewOrder[M] = Order[n];                      // duplicate this value
    	for (int i=M; i < Order.length; i++) {
    		NewOrder[i+1] = Order[i];
    	}
    	Order = NewOrder;
    }

}
