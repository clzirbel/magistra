// DictionaryActionListener.java

import java.awt.*;
import java.awt.event.*;

class DictionaryActionListener implements ActionListener {

    private WordList WL;
    private String[] Selected;
    private int n, L;
    private WordPair WP;
    private TextField baseWord, foreignWord, group, remove;
    private TextArea baseDisplay, foreignDisplay;

    DictionaryActionListener ( WordList WL, TextField baseWord, TextField foreignWord, TextField group, TextArea baseDisplay, TextArea foreignDisplay, int L, TextField remove)  {
	this.WL = WL;
	this.baseWord = baseWord;
	this.foreignWord = foreignWord;
	this.group = group;
	this.baseDisplay = baseDisplay;
	this.foreignDisplay = foreignDisplay;
    this.remove = remove;
    }

    public void actionPerformed (ActionEvent e) {
	if (e.getActionCommand().equals("Exit")) {
	    WL.writeWordList();
            System.exit(0);
	}
        else if (e.getSource().equals(foreignWord) | e.getSource().equals(group)) {
	    int m = WL.getMaxIndex()+1;

            WordPair newpair = new WordPair(baseWord.getText(),foreignWord.getText(),Integer.parseInt(group.getText()));

            WL.addPair( String.valueOf(m), newpair );

            if (!remove.getText().equals("No")) {
            	WP = WL.getPair(remove.getText());
            	WP.setGroup(-1);
            	remove.setText("No");
            }
            
	    baseWord.setText("");
	    foreignWord.setText("");
	    baseDisplay.setText("");
	    foreignDisplay.setText("");
	    baseWord.requestFocus();
	}
        else if (e.getSource().equals(foreignWord)) {
	    baseWord.requestFocus();
	}
        else if (e.getActionCommand().equals("Clear")) {
        	remove.setText("No");
	    baseWord.setText("");
	    foreignWord.setText("");
	    baseDisplay.setText("");
	    foreignDisplay.setText("");
	    foreignWord.requestFocus();
	}            
	}
}
