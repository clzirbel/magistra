// PracticeListener.java

import javax.swing.*;
import java.awt.event.*;

class PracticeListener implements ActionListener {

    private WordList WL;
    private String[] Selected;
    private int n;
    private int L;
    private WordPair WP;
    private JLabel baseLang, baseWord, foreignLang, status, help;
    private JTextField input;

    PracticeListener ( WordList WL, int n, int L, WordPair WP, JLabel baseLang, JLabel baseWord, JLabel foreignLang, JTextField input, JLabel status, JLabel help) {
	this.WL = WL;
//	this.Selected = Selected;
        this.n = n;
        this.L = L;
	this.WP = WP;
	this.baseLang = baseLang;
	this.baseWord = baseWord;
	this.foreignLang = foreignLang;
	this.input = input;
	this.status = status;
	this.help = help;
    }

    public void actionPerformed (ActionEvent e) {
	if (e.getActionCommand().equals("Switch direction")) {
	    L = 1 - L;
  	    n++;
	    WP = WL.getSelectedPair(n);
            baseLang.setText(WL.getLanguage(L));
            baseWord.setText(WP.getWord(L));
            foreignLang.setText(WL.getLanguage(1-L));
            input.setText("");
	}
	else if (e.getActionCommand().equals("Exit")) {
	    WL.writeUserData();
            System.exit(0);
	}
	else if (e.getActionCommand().equals("Skip once")) {
		n++;
	    WP = WL.getSelectedPair(n);
        baseLang.setText(WL.getLanguage(L));
        baseWord.setText(WP.getWord(L));
        foreignLang.setText(WL.getLanguage(1-L));
        input.setText("");
        status.setText("You know " + WL.getNumKnown() + " words.  Group " + WP.getGroup() + " " + WP.getUserData());
        help.setText("");
    }
	else if (e.getActionCommand().equals("Skip forever")) {
		n++;
		WP.setFirstResult('f');
		WP = WL.getSelectedPair(n);
        baseLang.setText(WL.getLanguage(L));
        baseWord.setText(WP.getWord(L));
        foreignLang.setText(WL.getLanguage(1-L));
        input.setText("");
        status.setText("You know " + WL.getNumKnown() + " words.  Group " + WP.getGroup() + " " + WP.getUserData());
        help.setText("");
   }
	else {
		 JTextField inputString = (JTextField)e.getSource();
         if (WP.compareStrings( 1-L, inputString.getText())) {  // correct answer
	     if ((L==0) && (WP.getNumTries() == 0)) {           // correct answer on first attempt
	    	 WP.setFirstResult('+');
           	 WL.changeNumKnown(UserData.evaluatePairData(WP.getUserData()+"+")-UserData.evaluatePairData(WP.getUserData()));
	     }
	     else if (WP.getNumTries() == 0)   // correct answer, but translating the "easy" direction
	    	 WP.setFirstResult('#');
	     // Move on to next word pair
	     n++;
	     WP = WL.getSelectedPair(n);
         baseLang.setText(WL.getLanguage(L));
         baseWord.setText(WP.getWord(L));
         foreignLang.setText(WL.getLanguage(1-L));
         input.setText("");
         status.setText("You know " + WL.getNumKnown() + " words.  Group " + WP.getGroup() + " " + WP.getUserData());
         help.setText("");
	 }
         else {                                  // incorrect answer
	     if (L==0) {
               WP.setFirstResult('-');
               WL.changeNumKnown(UserData.evaluatePairData(WP.getUserData()+"-")-UserData.evaluatePairData(WP.getUserData()));
	     }
	     else WP.setFirstResult('=');
	      WP.registerTry();
          input.setText("");
          help.setText(WP.getWord(1-L));
	  //          long startTime = System.currentTimeMillis();
	  //          while (System.currentTimeMillis() < startTime + 1);
	}
	}
    }
}


