// DictionaryListener.java

import java.awt.*;
// import javax.swing.*;
import java.awt.event.*;

class DictionaryListener implements TextListener {
	
    private WordList WL;
    private WordPair WP;
    private TextField baseWord, foreignWord, group;
    private TextArea baseDisplay, foreignDisplay;
    private TextField remove;
    private int[] foundarray;
    private int beingedited;
    
    DictionaryListener ( WordList WL, TextField baseWord, TextField foreignWord, TextField group, TextArea baseDisplay, TextArea foreignDisplay, TextField editentry, TextField changegroup, TextField remove, int[] foundarray, int beingedited)  {
	this.WL = WL;
	this.baseWord = baseWord;
	this.foreignWord = foreignWord;
	this.group = group;
	this.baseDisplay = baseDisplay;
	this.foreignDisplay = foreignDisplay;
    this.remove = remove;
    this.foundarray = foundarray;
    this.beingedited = beingedited;
    }

    public void textValueChanged (TextEvent e) {
        TextField tf = (TextField) e.getSource();
        String text = tf.getText();
	    int numfound = 0;
	    int current = 0;
        int chosen = 0;
        StringBuffer baseBuffer = new StringBuffer();
        StringBuffer foreignBuffer = new StringBuffer();

        for (int w=0; w < foundarray.length; w++) 
        	foundarray[w] = -1;
        
        if (tf.equals(baseWord) && text.length() == 1 && 
    	       text.compareTo("1") >= 0 && text.compareTo("9") <= 0) {

    	    	String ftext = foreignWord.getText();
    	    	chosen = Integer.parseInt(text.trim());

    	    	while ((numfound <= chosen-1) & (current < WL.getNumPairs())) {
    			WP = WL.getPairByNumber(current);
    			if (WP.containsString( 1, ftext)) {
    			    numfound++;
    			    current++;
    			}
    			else {
    				current++;
    			    }
    		    }
    	    	foreignWord.setText(WP.getWord(1));
    	    	baseWord.setText(WP.getWord(0));
                remove.setText(WL.getIndex(current-1));
        }
	    else if (tf.equals(baseWord) & text.length() > 0) {
		    while ((numfound < 20) & (current < WL.getNumPairs())) {
			WP = WL.getPairByNumber(current);
			if (WP.containsString( 0, text)) {
                foundarray[numfound] = current;
			    numfound++;
			    current++;
                baseBuffer.append( WP.getWord(0) ).append(" [Group ").append(WP.getGroup()).append("]").append( '\n' );
                foreignBuffer.append("["+numfound+"] ").append( WP.getWord(1) ).append( '\n' );
			}
			else {
				current++;
			    }
		    }
		    System.out.println("Found these indices: ");
		    for (int w=0; w < numfound; w++)
		    	System.out.print(foundarray[w]+" ");
		    System.out.println("");
	    }
	    else if (tf.equals(foreignWord) && text.length() == 1 && 
   	       text.compareTo("1") >= 0 && text.compareTo("9") <= 0) {

	    	String btext = baseWord.getText();
	    	chosen = Integer.parseInt(text.trim());

	    	while ((numfound <= chosen-1) & (current < WL.getNumPairs())) {
			WP = WL.getPairByNumber(current);
			if (WP.containsString( 0, btext)) {
			    numfound++;
			    current++;
			}
			else {
				current++;
			    }
		    }
	    	foreignWord.setText(WP.getWord(1));
	    	baseWord.setText(WP.getWord(0));
            remove.setText(WL.getIndex(current-1));
	    }
	    else if (tf.equals(foreignWord) & text.length() > 0) {
		    while ((numfound < 20) & (current < WL.getNumPairs())) {
				WP = WL.getPairByNumber(current);
				if (WP.containsString( 1, text)) {
		            foundarray[numfound] = current;
				    numfound++;
				    current++;
		            baseBuffer.append( WP.getWord(0) ).append(" [Group ").append(WP.getGroup()).append("]").append( '\n' );
		            foreignBuffer.append("["+numfound+"] ").append( WP.getWord(1) ).append( '\n' );
				}
				else {
					current++;
				    }
		    }
		    System.out.println("Found these indices: ");
		    for (int w=0; w < numfound; w++)
		    	System.out.print(foundarray[w]+" ");
		    System.out.println("");
    
	    }

        baseDisplay.setText( baseBuffer.toString() );
        foreignDisplay.setText( foreignBuffer.toString());
    }
}


