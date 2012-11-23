import java.io.File;

// Magistra.java 

class Magistra {
    public static void main(String[] args) 
    {
    	// args[0] is the language
    	// args[1] is the user's name
    	// args[2] tells what group to start with, and other things
    	// args[3] tells where the dictionary files are stored
    	// args[4] tells where the user files are stored
    	
    	Magistra m = new Magistra();

    	m.run(args[0], args[1], args[2], args[3], args[4]);
    }
    
    public void run(String name, String language, String levelText, String dictionarypath, String userfilepath)
    {

    System.out.println("Magistra was called with:");
    System.out.println("Language:  " + language);
    System.out.println("Name    :  " + name);
    System.out.println("Level   :  " + levelText);
    System.out.println("DPath   :  " + dictionarypath);
    System.out.println("UPath   :  " + userfilepath);
    	
	int i, numSelected, PriorityType;

	int level;
	try {
		level = Integer.parseInt(levelText);
	}
	catch(NumberFormatException e) {
		System.out.println("Using level 0");
		level = 0;
	}

	String wordlistfile;
	
	if (dictionarypath.length() == 0)
		wordlistfile = "pair_lists" + File.separator + language+".txt";
	else
		wordlistfile = dictionarypath + File.separator + language+".txt";

	WordList WL = new WordList(wordlistfile);

	System.out.println("Read " + wordlistfile);

	String userdatafile;
	
	if (userfilepath.length() == 0)
		userdatafile = name + "-"+language+".txt";
	else
		userdatafile = userfilepath + File.separator + name + "-"+language+".txt";

	UserData UD = new UserData(userdatafile);
	    
	WL.incorporateUserData(UD);

	String[] Selected = new String[9999];

    Selected = WL.getAllIndices();  // modify later for each user ...
	numSelected = WL.getNumPairs();

	WL.setSelected(Selected, numSelected);

    WL.setPriorities(level);
    WL.setOrder(numSelected);

    Practice P = new Practice(WL);
    }
}
