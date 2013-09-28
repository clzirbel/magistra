// DictionaryActionListener.java

import java.awt.*;
import java.awt.event.*;

class DictionaryActionListener implements ActionListener {

    private WordList WL;
    private WordPair WP;
    private TextField baseWord, foreignWord, group, remove, editentry, changegroup;
    private TextArea baseDisplay, foreignDisplay;
    private int[] foundarray;
    private boolean clearfields = false;
    private int beingedited;
    
    DictionaryActionListener ( WordList WL, TextField baseWord, TextField foreignWord, TextField group, TextArea baseDisplay, TextArea foreignDisplay, TextField editentry, TextField changegroup, TextField remove, int[] foundarray, int beingedited)  {
	this.WL = WL;
	this.baseWord = baseWord;
	this.foreignWord = foreignWord;
	this.group = group;
	this.baseDisplay = baseDisplay;
	this.foreignDisplay = foreignDisplay;
	this.editentry = editentry;
	this.changegroup = changegroup;
    this.remove = remove;
    this.foundarray = foundarray;
    this.beingedited = beingedited;
    }

    public void actionPerformed (ActionEvent e) {
	if (e.getActionCommand().equals("Save and Exit")) {
		WL.writeWordList();
        System.exit(0);
	}
    else if (e.getSource().equals(baseWord) | e.getSource().equals(group)) {
    	if (beingedited > -1) {          // editing a word pair
    		WordPair editedpair = WL.getPairByNumber(beingedited);
    		editedpair.setBaseWord(baseWord.getText());
    		editedpair.setForeignWord(foreignWord.getText());
    		editedpair.setGroup(Integer.parseInt(group.getText()));
    	}
    	else {                           // adding a new word pair
    		int m = WL.getMaxIndex()+1;
            WordPair newpair = new WordPair(baseWord.getText(),foreignWord.getText(),Integer.parseInt(group.getText()));
            WL.addPair( String.valueOf(m), newpair );
    	}
        clearfields = true;
	}
    else if (e.getSource().equals(foreignWord)) {
	    baseWord.requestFocus();
	}
    else if (e.getActionCommand().equals("Clear")) {
    	clearfields = true;
	}            
    else if (e.getSource().equals(editentry)) {
	    int w = Integer.parseInt(editentry.getText());
	    if (w > 0 & w < foundarray.length+1) {
	    	if (foundarray[w-1] > -1) {
	    		WordPair WP = WL.getPairByNumber(foundarray[w-1]);
	    	    baseWord.setText(WP.getWord(0));
	    	    foreignWord.setText(WP.getWord(1));
	    	    group.setText(Integer.toString(WP.getGroup()));
	    	    editentry.setText("Being edited currently");
	    	    beingedited = foundarray[w-1];
	    	}
	    }
    }
    else if (e.getSource().equals(changegroup)) {
	    int w = Integer.parseInt(changegroup.getText());
	    if (w > 0 & w < foundarray.length+1) {
	    	if (foundarray[w-1] > -1) {
	    		WordPair WP = WL.getPairByNumber(foundarray[w-1]);
	    		int v = Integer.parseInt(group.getText());
	    		if (v > 0) {
	    			WP.setGroup(v);
	    			clearfields = true;
	    		}
	    	}
	    }
    }
    else if (e.getSource().equals(remove)) {
	    System.out.println("These indices are available: ");
	    for (int w=0; w < foundarray.length; w++)
	    	System.out.print(foundarray[w]+" ");
	    System.out.println("");

	    int w = Integer.parseInt(remove.getText());
	    if (w > 0 & w < foundarray.length+1) {
	    	if (foundarray[w-1] > -1) {
	    		System.out.println("Removing pair with index "+Integer.toString(foundarray[w-1]));
	    		WL.removePair(foundarray[w-1]);
	    		clearfields = true;
	    	}
	    }
	    
    }

    if (clearfields) {
	    baseWord.setText("");
	    foreignWord.setText("");
	    baseDisplay.setText("");
	    foreignDisplay.setText("");
	    editentry.setText("");
	    changegroup.setText("");;
	    remove.setText("");
	    foreignWord.requestFocus();
	    beingedited = -1;
    }
    }
}
