import java.io.File;

// Dictionary.java makes it easier to edit a word list.  Typing in either of the top two boxes
// will find all entries in that "column" which contain what you type.  This helps to find out
// whether or not the given word already exists in the list.  Matches appear in the boxes
// below.  In the right column, the group is indicated in brackets.
// There is some functionality that allows you to replace an existing entry, but I don't
// remember how it works.
// Filling in both top boxes and hitting enter will add them to the word pairs, with the
// indicated group number.

/* if you find that a word pair is already in
the list, but not in the group that you want, it seems hard to
reassign the pair to a new group.  Here is what you do; make the
group number the one you want.  Then search for a word.  If there
is a match, or multiple matches, count down the list.  To
reassign the group number of the first pair, tab (or shift tab)
and then hit 1.  Second pair, hit 2.  This will fill in the
blanks with the word pair that you wanted, then you can change
the group number by hitting enter.
*/
class Dictionary {
    public static void main(String[] args) {

		// args[0] is the language
		// args[1] tells where the dictionary files are stored

		String language = args[0];
		String dictionarypath = args[1];

		Dictionary d = new Dictionary();
		d.run(language,dictionarypath);

    }
    
    public void run(String language, String dictionarypath) {
		
		String wordlistfile;
		
		if (dictionarypath.length() == 0)
			wordlistfile = "pair_lists" + File.separator + language+".txt";
		else
			wordlistfile = dictionarypath + File.separator + language+".txt";
		
		WordList WL = new WordList(wordlistfile);
		System.out.println("Read " + wordlistfile);
	
		int i, numSelected, PriorityType;

		String[] Selected = new String[9999];
	    Selected    = WL.getAllIndices();  // work with all pairs
		numSelected = WL.getNumPairs();

        DictionaryInit P = new DictionaryInit(WL);
    }
}
