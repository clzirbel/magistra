// DictionaryListener.java

import java.awt.*;
// import javax.swing.*;
import java.awt.event.*;

class DictionaryListener implements TextListener {
	
    private WordList WL;
    private WordPair WP;
    private TextField baseWord, foreignWord;
    private TextArea baseDisplay, foreignDisplay;
    private int[] foundarray;
    
    DictionaryListener ( WordList WL, TextField baseWord, TextField foreignWord, TextArea baseDisplay, TextArea foreignDisplay, int[] foundarray, int beingedited)  {
	this.WL = WL;
	this.baseWord = baseWord;
	this.foreignWord = foreignWord;
	this.baseDisplay = baseDisplay;
	this.foreignDisplay = foreignDisplay;
    this.foundarray = foundarray;
    }

    public void textValueChanged (TextEvent e) {
        TextField tf = (TextField) e.getSource();
        String text = tf.getText();
	    int numfound = 0;
	    int current = 0;
        StringBuffer baseBuffer = new StringBuffer();
        StringBuffer foreignBuffer = new StringBuffer();

        for (int w=0; w < foundarray.length; w++) 
        	foundarray[w] = -1;
        
        if (tf.equals(baseWord) & text.length() > 0) {
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
	    }

        baseDisplay.setText( baseBuffer.toString() );
        foreignDisplay.setText( foreignBuffer.toString());
    }
}


